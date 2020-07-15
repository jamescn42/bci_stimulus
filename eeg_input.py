# Author: Eli Kinney-Lang
# Modified by James Chen
# University of Calgary

"""
Created on Wed Jun 17 16:02:49 2020

This script set will stream in SSVEP data from the publicly available dataset
on using SSVEP to control an exoskeleton.

This is a master script laying out each step needed. This will be converted
into individual functions from python, so that end-users can easily call them.

@author: Eli
"""

# Default imports
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import time

# MNE Specific imports
import mne
from mne.channels import make_standard_montage
from mne.preprocessing import ICA

# SKLearn Imports
# SKLearn Model Selection

from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold, StratifiedShuffleSplit, train_test_split
# SKLearn Preprocessing and Pipelines

from sklearn.pipeline import make_pipeline
# SKLearn Classification schemes

from sklearn.linear_model import LogisticRegression, SGDClassifier, LinearRegression

# Pyriemann Estimation and Analysis
from pyriemann.estimation import Covariances, ERPCovariances, XdawnCovariances
from pyriemann.spatialfilters import CSP
from pyriemann.tangentspace import TangentSpace
from pyriemann.classification import MDM
from pyriemann.classification import KNearestNeighbor as riem_KNN
from pyriemann.utils.viz import plot_confusion_matrix

# Lab Streaming Layer Imports
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_streams, resolve_byprop


class ReadEEG:
    def __init__(self, data_dir=r'C:\Users\James\Documents\Python\summer_research\dataset-ssvep-exoskeleton'):
        # Get list of all subjects in the master data directory
        self.dir_list = os.listdir(data_dir)
        # Remove the files which aren't subject names
        self.subj_list = [name for name in self.dir_list if not os.path.isfile(data_dir + '\\' + name) is True]

    def __get_subj_trial_data(self, subj_path_name,
                              data_dir=r'C:\Users\James\Documents\Python\summer_research\dataset-ssvep-exoskeleton'):
        """
        Get the trial information from a given subject.
        This has been set-up for the public dataset of SSVEP exoskeleton data,
        present at https://github.com/sylvchev/dataset-ssvep-exoskeleton

        Only .fif files will be analyzed from this at the moment.

        Parameters
        ----------
        subj_path_name : str, required
            This is the subject-specific name. Only returns the '/*_raw.fif' and
            '/*-eve.fif' values.
        data_dir : str, required.
            This is the full path to the data to analyze.
            The default NEEDS TO BE CHANGED FOR YOUR COMPUTER PATH.
            Current default is - 'D:\\Users\\Eli\\Documents\\Python Scripts\\Example_Data\\dataset-ssvep-exoskeleton-master'.

        Returns
        -------
        raw_data_path : List
            List of the full path to the raw data file, (_raw.fif).
        event_data_path : List
            List of the full path to the event file (-eve.fif).

        """
        # Concat the data_directory with the subject_name
        data_path = data_dir + '\\' + subj_path_name
        # Now pull up all of the raw data held in '_raw.fif' info paths
        raw_data_path = glob.glob(data_path + '/*_raw.fif')
        # Repeat for all of the event data held in '-eve.fif'
        event_data_path = glob.glob(data_path + '/*-eve.fif')
        # Return vals
        return raw_data_path, event_data_path

    def __get_raw_data(self, raw_data_path, montage_type='easycap-M1'):
        """
        Extract the raw data from the given data path. Currently supports only
        .fif, .edf and .gdf extension types.

        Parameters
        ----------
        raw_data_path : List (str)
            Full path to the raw data. List is expected as input type.
        montage_type : str, optional
            Electrode montage to use with the data. The default is 'easycap-M1'.

        Returns
        -------
        raw : mne.io raw datatype
            MNE ready raw data for processing.

        """

        # Import raw data from mne.io using read_raw_*** for whichever extension
        if raw_data_path[-3:] == 'fif':

            print('...Importing raw .fif file...')
            raw = mne.io.read_raw_fif(raw_data_path, preload=True)
        elif raw_data_path[-3:] == 'edf':
            print('...Importing raw .edf file...')
            raw = mne.io.read_raw_edf(raw_data_path, preload=True)
        elif raw_data_path[-3:] == 'gdf':
            print('...Importing raw .gdf file...')
            raw = mne.io.read_raw_gdf(raw_data_path, preload=True)
        else:
            print('WARNING!')
            print('Extension type not recognized for this function!')
            print('You will need to manually import the data via MNE!')
            print(' ')
            return
        # Add the montage information
        montage = make_standard_montage(montage_type)
        # Set the montage
        raw.set_montage(montage)
        # Return vals
        return raw

    def __get_event_data(self, event_data_path):
        """
        Extract the event data from a dedicated event file based on the given path.
        Currently only supports the .eve file extension.

        Parameters
        ----------
        event_data_path : List (str)
            Full path to the event data file. List is the expected input type.

        Returns
        -------
        events : Array of int32
            Event data structure in a format ready for MNE processing. Structure
            gives 3 columns for each event found - [timestamp, 0, event_type]

        """
        # Just run the one command line from NME to get event data.
        events = mne.read_events(event_data_path)
        return events

    def __get_mne_ready_data(self, raw_data_path, event_data_path, montage_type='easycap-M1'):
        """
        Extract raw and event data ready for MNE processing.

        Parameters
        ----------
        raw_data_path : List (str)
            Full path to the raw data. List is expected as input type.
        event_data_path : List (str)
            Full path to the event data file. List is the expected input type.
        montage_type : str, optional
            Electrode montage to use with the data. The default is 'easycap-M1'.

        Returns
        -------
        raw : mne.io raw datatype
            MNE ready raw data for processing.
        events : Array of int32
            Event data structure in a format ready for MNE processing. Structure
            gives 3 columns for each event found - [timestamp, 0, event_type]

        See Also
        --------
        get_raw_data
        get_event_data

        """
        # Get the raw data
        raw = self.__get_raw_data(raw_data_path, montage_type)
        # Get the event data
        events = self.__get_event_data(event_data_path)
        # Return vals
        return raw, events

    def __build_epochs(self, raw, events, tmin=3, tmax=8,
                       event_id=dict(resting=1, stim13=2, stim17=3, stim21=4),
                       picks_val='Default', notch_filt=True, bp_low=6, bp_high=25,
                       filt_method='iir', detrend_val=0, plot_raw_timeseries=False):
        """
        Process MNE ready raw data into event-defined epochs for classification.

        Parameters
        ----------
        raw : mne.io raw data
            Raw data to process.
        events : int32 array
            Array of event information, including timestamp and event value.
        tmin : int, optional
            Minimum value in seconds for epoch start wrt event marker. The default is 3.
        tmax : int, optional
            Maximum value in seconds for end of epoch wrt event marker. The default is 8.
        event_id : dict, optional
            Dictionary for event information. The default is dict(resting=1,stim13=2,stim17=3,stim21=4).
        picks_val : str, optional
            Type of 'pick' for MNE. The default is 'Default' which is for EEG data.
            Can be 'meg','eeg','stim' or 'eog' if not 'Default'. This is a MNE
            derived value. See mne.Epochs docstring for additional details.
        notch_filt : bool, optional
            Run notch filtering or not, at 50/60 Hz. The default is True.
        bp_low : int, optional
            Lower bound for bandpass filtering. The default is 6.
        bp_high : int, optional
            Upper boudn for bandpass filtering. The default is 25.
        filt_method : str, optional
            Type of filter to use. The default is 'iir'. Can also be 'fir'. Is MNE
            derived value. See mne.Epochs docstring for additional details.
        detrend_val : Int, optional
            MNE derived value for detrending raw data in each epoch. Can be either
            0 or 1. 0 is a constant (DC) detrend, 1 is a linear detrend. None is no
            detrending. See mne.Epochs docstring for additional details.
            The default is 1.
        plot_raw_timeseries : bool, optional
            Plot the raw time series data using MNE's plot.raw after filtering.
            The default is True.

        Returns
        -------
        epochs : Epoch object
            Returns MNE ready Epoch object. This can be used for further processing
            or plotting through MNE. Epochs are defined on provided event data.

        See Also
        --------
        mne.Epochs

        """

        print("...Starting pick determination...")
        # This whole section is optional. Picks may be a useful argument down the
        # road, but is currently just the default types.
        # Deal with what happens if picks is 'Default'.
        if picks_val.casefold() == 'Default'.casefold():
            picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False)
        # Deal with picks if it is given as a list
        elif type(picks_val) is list:
            # Set all to False to start with
            meg_bool, eeg_bool, stim_bool, eog_bool = False, False, False, False
            # Deal with each case for the List
            meg_bool = [True for pick in picks if pick.casefold() == 'meg']
            eeg_bool = [True for pick in picks if pick.casefold() == 'eeg']
            stim_bool = [True for pick in picks if pick.casefold() == 'stim']
            eog_bool = [True for pick in picks if pick.casefold() == 'eog']
            picks = mne.pick_types(raw.info, meg=meg_bool, eeg=eeg_bool, stim=stim_bool, eog=eog_bool)
        else:
            print('WARNING!!!! Your choice for `picks` variable was not recognized!/n')
            print('Please enter either `Default` or a list for the picks!')
            return

        # Print debug statements
        print("...Finished with picks...")
        print(" ")
        print('...Starting notch filtering...')
        # Just run a default notch filter at 60 Hz

        if notch_filt is True:
            raw.notch_filter(np.arange(60, 120, 60), picks=picks, filter_length='auto',
                             phase='zero')

            # Print debug statements
        print("...Finished with notch filtering...")
        print(" ")
        print('...Starting band pass filtering...')
        # Filter the time series based on a bandpass filter, with the given filt_method
        raw.filter(bp_low, bp_high, method=filt_method, picks=picks)

        print("...Finished with filtering...")

        # Plot the raw time-series.
        if plot_raw_timeseries is True:
            print(" ")
            print("...Starting a raw time-series plot...")

            # The plot options are hardcoded right now...need to fix later to be more flexible
            event_colors = {1: 'red', 2: 'blue', 3: 'green', 4: 'cyan'}
            eeg_color = {'eeg': 'steelblue'}
            scalings = {'eeg': 2e-2}
            n_chans_plot = 8
            duration = 40
            title = 'Raw EEG Time Series'
            start_time = 60
            # Plot the actual time series.
            raw.plot(events=events, event_color=event_colors, duration=duration,
                     n_channels=n_chans_plot, color=eeg_color, scalings=scalings,
                     show_options=False, title=title, start=start_time)

            print("...Plot made!...")

        print(" ")
        print('...Building epochs...')

        # Epoching and Artifact Rejection
        epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=False, baseline=None, picks=picks, preload=True,
                            detrend=0)

        # Return vals
        return epochs

    def __run_ica_rejection(self, epochs, n_components=None, random_state=42,
                            method='fastica', fit_params=None, max_iter=200,
                            make_plots=False):
        """
        Simple function for running ICA artifact rejection, based on hardcoded options.

        Parameters
        ----------
        epochs : Epoch object (MNE)
            MNE ready epochs to process. See 'build_epochs' for more details.
        n_components : int, optional
            Number of principal components passed to the ICA during fitting.
            See the mne.preprocessing.ICA docstring for more details.
            The default is None.
        random_state : int, optional
            The value to be used as the 'seed' for `numpy.random.RandomState`.
            See the mne.preprocessing.ICA docstring for more details.
            The default is 42.
        method : TYPE, optional
            ICA method to be used. Can be 'fastica', 'infomax', or 'picard'.
            See the mne.preprocessing.ICA docstring for more details.
            The default is 'fastica'.
        fit_params : dict, optional
            Additional parameters pased to the ICA estimator as specified by 'method'.
            See the mne.preprocessing.ICA docstring for more details.
            The default is None.
        max_iter : int, optional
            Maximum number of iterations during ICA fit.
            The default is 200.
        make_plots : bool, optional
            Plot the individual principal components found for the ICA.
            The default is False.

        Returns
        -------
        cleaned_epochs : Epoch object
            Returns an artifact cleaned MNE ready epoch object.

        See Also
        --------
        mne.preprocessing.ICA

        """

        if method.casefold() == 'infomax':
            fit_params = dict(extended=True)  # For extended infomax

        # We will use artificat rejection for each epoch through ICA.
        ica = ICA(n_components=n_components, random_state=random_state,
                  method=method, fit_params=fit_params, max_iter=max_iter)
        # Fit the ICA
        ica.fit(epochs)
        # Detect artifacts automatically
        ica.detect_artifacts(epochs)
        # Exclude based on detected artifacts
        ica.exclude
        print("The rejected ICA components were: " + str(ica.exclude))
        # This is just making basic plots right now. Will update later to be more thorough.
        if make_plots is True and n_components is None:
            nchans = ica.info['nchan']
            ica.plot_components()
            [ica.plot_properties(epochs, picks=[x]) for x in range(0, nchans)]
        elif make_plots is True:
            ncomps = n_components
            ica.plot_components()
            [ica.plot_properties(epochs, picks=[x]) for x in range(0, ncomps)]
        # Save to new data - not needed here, but kept just in case
        cleaned_epochs = epochs.copy()
        # Apply ICA rejections
        ica.apply(cleaned_epochs)

        return cleaned_epochs

    def __run_strat_validation_RG(self, epochs, n_strat_folds=5, shuffle=False,
                                  random_state=42, RG_Pipeline_Num=0,
                                  estimator='lwf',
                                  class_names=['Rest', '13 Hz', '17 Hz', '21 Hz'],
                                  accuracy_threshold=0.7):
        """
        Complete a stratified cross-validation using Riemannian Geometery pipeline.

        Parameters
        ----------
        epochs : Epoch Object from MNE
            Epoch data held in an appropriate MNE format. This could be derived from
            mne.Epochs, or using the `build_epochs` command included in this script.
        n_strat_folds : int, optional
            Number of folds for the stratified K-Fold cross-validation.
            This value should be chosen carefully to avoid unbalanced classes.
            The default is 5.
        shuffle : bool, optional
            Shuffle training set data. See sklearn.model_selection.StratifiedKFold
            for more details.
            The default is False.
        random_state : int, optional
            The value to be used as the 'seed' for `numpy.random.RandomState`.
            See sklearn.model_selection.StratifiedKFold for more details.
            The default is 42.
        RG_Pipeline_Num : int, optional
            Which pre-defined Riemannian Geometery pipeline to run for analysis.
            Can be 0,1,2,3:
                Pipeline 0:
                    Covariance w/ estimator -> Riemannian KNN
                Pipeline 1:
                    Covariance w/ estimator -> CSP -> TangentSpace -> LogisticRegression
                    LogReg uses a 'balanced' option for class weights, l2 penalty.
                Pipeline 2:
                    XDawnCovariance w/ estimator -> TangentSpace -> LogisticRegression
                    LogReg uses elasticnet penalty, solver soga and a multinominal multi_class flag.
                Pipeline 3:
                    Covariance w/ estimator -> MDM.
                    Minimum distance to mean (MDM) is the main classification scheme.
            The default is 0.
        estimator : str, optional
            Covariance matrix estimator to use. For regularization consider 'lwf'
            or 'oas'. For complete lists, see pyriemann.utils.covariance.
            The default is 'lwf'.
        class_names : List, optional
            List of names for the confusion matrix plot.
            The default is ['Rest','13 Hz','17 Hz','21 Hz'].
        accuracy_threshold : float, optional
            Threshold for determining which folds are 'good' fits. Accuracy found
            above the threshold (e.g. 70% or greater) will be reported as good fit
            folds.
            The default is 0.7.

        Returns
        -------
        DICT
            Dictionary of outputs are returned for the user.
            In order:
                Fold accuracy -'Fold Acc'
                Indices for `good` training folds > or = to accuracy_threshold value - 'Good Train Ind'
                Indices for `good` test folds > or = to given accuracy_threshold value -  'Good Test Ind'
                Indices for `bad` train folds < given accuracy_threshold value - 'Bad Train Ind'
                Indices for `bad` test folds < given accuracy_threshold value - 'Bad Test Ind'
                List of predicted classes from the RG Pipeline - 'Prediction List'
                List of true classes from the RG Pipeline - 'True Class List'

        See Also
        --------
        mne.Epochs
        sklearn.model_selection.StratifiedKFold
        sklearn.linear_model.LogisticRegression
        pyriemann.estimation.Covariances
        pyriemann.estimation.XdawnCovariances
        pyriemann.spatialfilters.CSP
        pyriemann.tangentspace.TangentSpace
        pyriemann.classification.MDM
        pyriemann.classification.KNearestNeighbor (riemmanian KNN)


        """

        # Set the stratified CV model
        cv_strat = StratifiedKFold(n_splits=n_strat_folds, shuffle=True,
                                   random_state=random_state)  # Requires us to input in the ylabels as well...need to figure out how to get this.

        # Run one of the pre-defined pipelines
        if RG_Pipeline_Num == 1:
            clf = make_pipeline(Covariances(estimator=estimator),
                                CSP(log=False), TangentSpace(),
                                LogisticRegression(class_weight='balanced',
                                                   max_iter=500))
        elif RG_Pipeline_Num == 2:
            clf = make_pipeline(XdawnCovariances(estimator=estimator,
                                                 xdawn_estimator=estimator),
                                TangentSpace(),
                                LogisticRegression(penalty='elasticnet', class_weight=None, solver='saga',
                                                   multi_class='multinomial', l1_ratio=0.5,
                                                   max_iter=500))
        elif RG_Pipeline_Num == 3:
            clf = make_pipeline(Covariances(estimator=estimator), MDM())  # This is the best so far
        else:
            print("...Running a default pipeline for RG using Covariance, and KNN...")
            clf = make_pipeline(Covariances(estimator=estimator), riem_KNN())

        # Get the labels for the data
        labels = epochs.events[:, -1]
        # Identify the data itself
        X_data = epochs.get_data()
        # Get the class names for the confusion matrix
        class_names = class_names

        # Make empty lists for each item in the stratified CV
        acc_list = []
        preds_list = []
        true_class_list = []
        good_train_indx = []
        good_test_indx = []
        bad_train_indx = []
        bad_test_indx = []

        # For loop testing each iteration of the stratified cross-validation
        for train_idx, test_idx in cv_strat.split(X_data, labels):
            # Get the x_train and x_test data for this fold
            x_train, x_test = X_data[train_idx], X_data[test_idx]
            # Get the y_train and y_test data for this fold
            y_train, y_test = labels[train_idx], labels[test_idx]
            # Fit the classifier
            clf.fit(x_train, y_train)
            # Find the predicted value on the test data in this fold
            preds = clf.predict(x_test)
            # Save in list
            preds_list.append(preds)
            # Save the true class labels in a list for this fold
            true_class_list.append(y_test)
            # Find the accuracy on average from this prediction
            acc_mean = np.average(preds == y_test)
            # Save the accuracy to a list
            acc_list.append(acc_mean)
            # Find out where the 'Good' training folds are. (Greater than threshold)
            if acc_mean >= accuracy_threshold:
                print("Train indices above accuracy threshold of " + str(accuracy_threshold * 100) + "% are: ",
                      train_idx)
                print("Test indices above accuracy threshold of " + str(accuracy_threshold * 100) + "% are: ", test_idx)
                good_train_indx.append(train_idx)
                good_test_indx.append(test_idx)
            # Find out where the 'Bad' training folds are. (Less than threshold)
            else:
                bad_train_indx.append(train_idx)
                bad_test_indx.append(test_idx)
            # Make a plot for the confusion matrix
            fig = plt.figure()
            plot_confusion_matrix(y_test, preds, class_names)
        # Print out the final results from across all folds on average
        print("The overall accuracy with " + str(n_strat_folds) + "-fold stratified CV was: ", np.average(acc_list))

        # Return output vals
        return dict({'Fold Acc': acc_list, 'Good Train Ind': good_train_indx,
                     'Good Test Ind': good_test_indx, 'Bad Train Ind': bad_train_indx,
                     'Bad Test Ind': bad_test_indx, 'Prediction List': preds_list,
                     'True Class List': true_class_list})

    def __train_predefined_classifier(self, epochs, RG_Pipeline_Num=0, estimator='lwf',
                                      estimate_accuracy=False, random_state=44,
                                      class_names=['Rest', '13 Hz', '17 Hz', '21 Hz']):
        """
        Train a predefined Riemannian Geometery pipeline on a single dataset using
        MNE and pyriemann.

        Parameters
        ----------
        epochs : Epoch Object from MNE
            Epoch data held in an appropriate MNE format. This could be derived from
            mne.Epochs, or using the `build_epochs` command included in this script.
        RG_Pipeline_Num :int, optional
            Which pre-defined Riemannian Geometery pipeline to run for analysis.
            Can be 0,1,2,3:
                Pipeline 0:
                    Covariance w/ estimator -> Riemannian KNN
                Pipeline 1:
                    Covariance w/ estimator -> CSP -> TangentSpace -> LogisticRegression
                    LogReg uses a 'balanced' option for class weights, l2 penalty.
                Pipeline 2:
                    XDawnCovariance w/ estimator -> TangentSpace -> LogisticRegression
                    LogReg uses elasticnet penalty, solver soga and a multinominal multi_class flag.
                Pipeline 3:
                    Covariance w/ estimator -> MDM.
                    Minimum distance to mean (MDM) is the main classification scheme.
            The default is 0.
        estimator :  str, optional
            Covariance matrix estimator to use. For regularization consider 'lwf'
            or 'oas'. For complete lists, see pyriemann.utils.covariance.
            The default is 'lwf'.
        estimate_accuracy : bool, optional
            Estimate model accuracy roughly using a simple data-hold out train/test split.
            A default hold out of 75/25% train, test respectively is used.
            The default is False.
        random_state : int, optional
            The value to be used as the 'seed' for `numpy.random.RandomState`.
            See sklearn.model_selection.StratifiedKFold for more details.
            The default is 42.
        class_names : List, optional
            List of names for the confusion matrix plot.
            The default is ['Rest','13 Hz','17 Hz','21 Hz'].

        Returns
        -------
        clf : Classifier object (sklearn)
            Returns a trained classifier object based on the given epoch data and
            Riemannian Geometry pipeline.
        See Also
        --------
        mne.Epochs
        sklearn.model_selection.StratifiedKFold
        sklearn.linear_model.LogisticRegression
        pyriemann.estimation.Covariances
        pyriemann.estimation.XdawnCovariances
        pyriemann.spatialfilters.CSP
        pyriemann.tangentspace.TangentSpace
        pyriemann.classification.MDM
        pyriemann.classification.KNearestNeighbor (riemmanian KNN)

        """

        # Run one of the pre-defined pipelines
        if RG_Pipeline_Num == 1:
            clf = make_pipeline(Covariances(estimator=estimator),
                                CSP(log=False), TangentSpace(),
                                LogisticRegression(class_weight='balanced',
                                                   max_iter=500))
        elif RG_Pipeline_Num == 2:
            clf = make_pipeline(XdawnCovariances(estimator=estimator,
                                                 xdawn_estimator=estimator),
                                TangentSpace(),
                                LogisticRegression(penalty='elasticnet', class_weight=None, solver='saga',
                                                   multi_class='multinomial', l1_ratio=0.5,
                                                   max_iter=500))
        elif RG_Pipeline_Num == 3:
            clf = make_pipeline(Covariances(estimator=estimator), MDM())  # This is the best so far
        else:
            print("...Running a default pipeline for RG using Covariance, and KNN...")
            clf = make_pipeline(Covariances(estimator=estimator), riem_KNN())

        # Get the labels for the data
        labels = epochs.events[:, -1]
        # Identify the data itself
        X_data = epochs.get_data()
        # Get the class names for the confusion matrix
        class_names = class_names

        # This is NOT a great measure of the model accuracy. This just will give you
        # a rough estimate of how it is performing within its own dataset. This
        # should be used sparingly!
        if estimate_accuracy is True:
            # Do a simple data-hold out for testing
            x_train, x_test, y_train, y_test = train_test_split(X_data, labels, test_size=0.25,
                                                                random_state=random_state)

            clf_estimate = clf

            clf_estimate.fit(x_train, y_train)

            pred_vals = clf_estimate.predict(x_test)

            accuracy_val = np.mean(pred_vals == y_test)

            fig = plt.figure()
            plot_confusion_matrix(y_test, pred_vals, class_names)

        # Fit the data to the given epoch information
        clf.fit(X_data, labels)

        return clf

    def __setup_output_stream(self, stream_name, stream_type):
        """
        Initialize a LSL outlet of particular name and type

        Parameters
        ----------
        stream_name : str
            Name of LSL outlet to initialize. Can be anything.
        stream_type : str
            Type of LSL outlet to initialze. Typical choices are 'marker', 'data',
            or 'eeg'.

        Returns
        -------
        outlet : LSL Outlet
            Creates a LSL-ready outlet for streaming data over the network.

        """
        # Identify the type of data we are sending back.
        if stream_type.casefold() == 'marker'.casefold():
            info = StreamInfo(stream_name, stream_type, channel_count=1,
                              nominal_srate=0, channel_format='string',
                              source_id='single314uid')
        elif stream_type.casefold() == 'data'.casefold():
            info = StreamInfo(stream_name, stream_type, channel_count=1,
                              nominal_srate=0,
                              source_id='single314uid')

        # Make the stream outlet using the infor provided above
        print('...setting up LSL outlet object...')
        outlet = StreamOutlet(info)

        return outlet

    def __stream_class_output(self, data_to_stream, outlet, init_stream=False,
                              stream_name='PythonOut', stream_type='Marker'):
        """
        Stream data from python to the network using LSL outlet.

        Parameters
        ----------
        data_to_stream : np.ndarray|list|str
            Data that will be streamed to the network.
        outlet : LSL Outlet
            LSL outlet object used to stream the data. See setup_output_stream and
            pylsl.StreamOutlet for more information.
        init_stream : bool, optional
            Initialize an outlet stream using the 'setup_output_stream' function.
            The default is False.
        stream_name : str, optional
            Name of stream for the outlet. ONLY REQUIRED IF INIT_STREAM IS TRUE!
            The default is 'PythonOut'.
        stream_type : str, optional
            Type of outlet stream to be used. ONLY REQUIRED IF INIT_STREAM IS TRUE!
            The default is 'Marker'.

        Returns
        -------
        None. The LSL outlet is used to stream this data.

        See Also
        --------
        pylsl.StreamOutlet

        """

        if init_stream == True:
            outlet = self.__setup_output_stream(stream_name, stream_type)

        # Print statment this is working
        print('...sending predicted class via LSL outlet...')

        # How to send the data if it is in an Numpy Array or list
        if isinstance(data_to_stream, np.ndarray) or isinstance(data_to_stream, list):
            print('...Output data held as a numeric, sending to LSL...')
            # List comprehension to print each class prediction in the numpy array as a string
            [outlet.push_sample(str(class_pred)) for class_pred in data_to_stream]
            # Debug print statement!
            [print('DEBUG: This was sent to LSL: ' + str(class_pred)) for indx, class_pred in enumerate(data_to_stream)]

        elif isinstance(data_to_stream, str):
            print('...Output data held as a string, sending to LSL...')
            [outlet.push_sample(str(class_pred)) for class_pred in data_to_stream]
            # Debug print statement!
            [print('DEBUG: This was sent to LSL: ' + str(class_pred)) for indx, class_pred in enumerate(data_to_stream)]

        else:
            print('...Output data not recognized - trying something else...')
            # Haven't actually tried anything new here - will work on this when
            # such a bug happens.
            [outlet.push_sample(str(class_pred)) for class_pred in data_to_stream]
            [print('DEBUG: This was sent to LSL: ' + str(class_pred)) for indx, class_pred in enumerate(data_to_stream)]

        # Return output vals
        return

    def __stream_in_class(self, prop_to_search, name_to_search, active_time=60, timeout_for_resolve=15):
        """
        Create LSL inlet and stream in data from LSL outlet of given property and
        name.

        Parameters
        ----------
        prop_to_search : str
            Property type to search for a LSL outlet. Typical properties include
            'eeg','marker','data'.
        name_to_search : str
            Name of LSL outlet to search
        active_time : int, optional
            Time in seconds to actively stream in data from LSL outlet.
            The default is 60.
        timeout_for_resolve : int, optional
            Time in seconds to wait on searching for a given LSL outlet stream with
            the given property type and name.
            The default is 15.

        Returns
        -------
        sample_list : List
            List of data read into the LSL inlet from LSL outlet.
        timestamp_list : List
            List of time stamps for each specific sample read in from the LSL outlet.

        """
        # Find active streams
        print("...Searching for active streams...")
        active_streams = resolve_byprop(prop=prop_to_search, value=name_to_search, timeout=timeout_for_resolve)

        if not active_streams:
            print(" ")
            print("...WARNING!!...")
            print("...No active streams found!...")
            print("...Stopping function...")
            print(" ")
            return

        print("...Streams found!...")
        inlet = StreamInlet(active_streams[0])
        sample_list = []
        timestamp_list = []

        if active_time is not bool:
            # Get the start time
            tstart = time.time()

            print("...Starting to pull samples...")

            while time.time() < tstart + active_time:
                # Print that the stream was found!

                # Pull the sample
                sample, timestamp = inlet.pull_sample()
                sample_list.append(sample)
                timestamp_list.append(timestamp)
                # Return output vals
                print('Predicted value is: ' + str(sample))

            # Let them know the active stream is shutting down!
            print("...Active stream active time is done! Stopping stream...")

        else:
            # Find when this loop started
            tstart = time.time()
            max_runtime = 60 * 60 * 4  # This is 4 hours of sampling

            print("...Starting to pull samples...")

            while active_time is True:

                sample, timestamp = inlet.pull_sample()
                sample_list.append(sample)
                timestamp_list.append(timestamp)
                # Return output vals
                print('Predicted value is: ' + str(sample))

                # Maximum run condition for the moment to avoid permanently locking the system.
                if time.time() > tstart + max_runtime:
                    break
                print("...Active stream timed out! Stopping stream...")

        # Return output vals
        print("...All streams finished! Ending function...")
        return sample_list, timestamp_list

    def simulate_SSVEP_pipeline(self, train_subj, test_subj, simulate_online=False,
                                return_speed=1,
                                trn_trial=0, tst_trial=0,
                                run_validation=False, pipeline=1,
                                stream_name='PythonOut', stream_type='Marker'):
        """
        Run through and simulate a full processing pipeline based on the SSVEP exo-
        skeleton dataset. This assummes you have the given subject data of interest
        in a list, with the full path to the subject data.

        Parameters
        ----------
        train_subj : int
            Subject number to use for training the online model, based on a list
            of subjects for analysis. Such a list MUST include the full path to
            each given subject, including raw and event data.
        test_subj : int
            Subject number to use for testing the online model, based on a list
            of subjects for analysis. Such a list MUST include the full path to
            each given subject, including raw and event data.
        simulate_online : bool, optional
            Start the simulation of 'online' data using LSL inlet/outlet streams.
            The default is False.
        return_speed : int, optional
            Time in seconds to wait between streaming data in online simulation.
            The default is 1.
        trn_trial : int, optional
            Trial number to be used in training the model.
            The default is 0.
        tst_trial : int, optional
            Trial number to be used in assessing and testing the trained model.
            The default is 0.
        run_validation : bool, optional
            Run a stratified cross-fold validation of the trained model. This uses
            the 'run_strat_validation' function above.
            The default is False.
        pipeline : int, optional
            Which pre-defined Riemannian Geometery pipeline to run for analysis.
            Can be 0,1,2,3:
                Pipeline 0:
                    Covariance w/ estimator -> Riemannian KNN
                Pipeline 1:
                    Covariance w/ estimator -> CSP -> TangentSpace -> LogisticRegression
                    LogReg uses a 'balanced' option for class weights, l2 penalty.
                Pipeline 2:
                    XDawnCovariance w/ estimator -> TangentSpace -> LogisticRegression
                    LogReg uses elasticnet penalty, solver soga and a multinominal multi_class flag.
                Pipeline 3:
                    Covariance w/ estimator -> MDM.
                    Minimum distance to mean (MDM) is the main classification scheme.
            The default is 1.
        stream_name : str, optional
            Name of stream LSL outlet. ONLY REQUIRED IF SIMULATE_ONLINE IS TRUE!
            The default is 'PythonOut'.
        stream_type : str, optional
            Type of stream LSL outlet. ONLY REQUIRED IF SIMULATE_ONLINE IS TRUE!
            The default is 'Marker'.

        Returns
        -------
        dict({'Predicted','True_Vals'})
            Returns a dictionary with 2 kewords.
                Predicted - Predicted values of the processing pipeline.
                True_Vals - True values for the actual test data for comparison.

        """

        # First check if the train_subj and test_subj are the same
        if train_subj == test_subj:
            print("NOTICE!")
            print("...You have put in the same train and test subject!")
            print("...Making sure the train and test trials are not the same...")
            if trn_trial == tst_trial:
                print('WARNING!')
                print('...The train trial and test were found to be the same!')
                print('...Changing the value of the test trial...')
                if trn_trial == 0:
                    tst_trial = 1
                elif trn_trial == 1:
                    tst_trial = 0

        ##Get the training data path
        trn_data_path, trn_event_path = self.__get_subj_trial_data(self.subj_list[train_subj])

        # Get the training data from the first recording
        train_raw, train_events = self.__get_mne_ready_data(trn_data_path[trn_trial], trn_event_path[trn_trial])

        trn_epochs = self.__build_epochs(train_raw, train_events)

        # If run validation is true, then we will validate the pipeline as before
        if run_validation == True:
            trn_validation = self.__run_strat_validation_RG(trn_epochs, n_strat_folds=4, RG_Pipeline_Num=pipeline)

        clf_trained = self.__train_predefined_classifier(trn_epochs, RG_Pipeline_Num=pipeline, estimate_accuracy=False)

        ##Get the testing data path
        test_data_path, test_event_path = self.__get_subj_trial_data(self.subj_list[test_subj])

        # Get the testing data from the next recording
        test_raw, test_events = self.__get_mne_ready_data(test_data_path[tst_trial], test_event_path[tst_trial])

        test_epochs = self.__build_epochs(test_raw, test_events)

        # Apply this now on the train classifier
        predicted = clf_trained.predict(test_epochs.get_data())

        # If true, then we will 'simulate' running online function, by steadily
        # returning values slowly.
        if simulate_online == True:
            outlet = self.__setup_output_stream('Sim_Prediction', 'Marker')
            for pred in predicted:
                # Use the LSL streaming function above
                output_pred = str(pred)
                # print('..The type of marker is-')
                # print(type(output_pred))
                self.__stream_class_output(output_pred, outlet, stream_name, stream_type)
                print("Predicted Value: " + str(pred))
                time.sleep(return_speed)

            # Delete the outlet
            # print('...Deleting the outlet...')
            # outlet.__del__()

        # Just give some basic output about accuarcy
        true_val = test_epochs.events[:, -1]
        accuracy = np.mean(predicted == test_epochs.events[:, -1])
        print("...The overall predicted accuracy is " + str(accuracy))

        return dict({'Predicted': predicted, 'True_Vals': true_val})


if __name__ == '__main__':
    test = ReadEEG()
    test.simulate_SSVEP_pipeline(train_subj=5, test_subj=5,
                                 simulate_online=True,
                                 trn_trial=0, tst_trial=1,
                                 pipeline=2, return_speed=0.1)
