from sklearn.ensemble import RandomForestClassifier;
import pandas as pd;
import numpy as np;
import sys;


##########################################################################
## Load Inputs and HPs
##########################################################################
#########################################################
## Read Arguments
#########################################################
if(sys.argv[1] == "-h"):
    print ("name source_mod njobs");
    exit();
arguments = dict();
acceptable_arguments = ['name', 'source_mod', 'njobs'];
for i in range(len(sys.argv)):
    if(i == 0):
        continue;
    this_argv = sys.argv[i];
    parts = this_argv.split(":");
    this_name = parts[0];
    this_value = parts[1];
    if(this_name not in acceptable_arguments):
        print(this_name, " is not an acceptable argument. Error.");
        exit();
    arguments[this_name] = this_value;
    

#########################################################
## Set Default Data
#########################################################
NJOBS = 2;

#########################################################
## Update data to arguments
#########################################################
if('name' in arguments):
    delta_mod = arguments['name'];
else:
    print("name is required. Error.");
    exit();
if('source_mod' in arguments):
    source_mod = arguments['source_mod'];
    TRAIN_SOURCE = '../../1_split_data/results/' + source_mod +'_train.csv';
    TEST_SOURCE = '../../1_split_data/results/' + source_mod +'_test.csv';
else:
    print("source_mod is required. Error.");
    exit();
if('njobs' in arguments): NJOBS = int(arguments['njobs']);
    
    
#############################################################
## Load Data
##############################################################
def load_data_set(data_source_path):
    with open(data_source_path) as fp:
        source_lines = fp.readlines();
    batch_data_length = len(source_lines) - 1;
    keys_list = []; ## only supports one key per row atm
    y_data = [];
    feature_data = None; #numpy.zeros([batch_size, len(feature_index)], 'float');
    ## Grab and parse data

    for index, line in enumerate(source_lines):
        parts = line.rstrip().split(",");
        if(parts[0] == 'label'):
            continue; # header row
        this_label = int(float(parts[0]));
        this_word = parts[1];
        this_vector = np.array([float(j) for j in parts[2:]])

        if(feature_data is None):
            feature_data = np.zeros([batch_data_length, len(this_vector)], 'float');

        keys_list.append(this_word);
        y_data.append(this_label); ## one hot encoding
        feature_data[len(keys_list)-1, :] = this_vector;

        if(index % 2000 == 0):
            print("at word ", index);

    return feature_data, y_data, keys_list;
        #if(i%100 == 0):
            #print(i);
            #print(len(keys_list));
            #print(feature_data.shape);    
##############################
## Load Train Data
##############################
print("Loading train and test data...");
train_features, train_labels, train_keys = load_data_set(TRAIN_SOURCE);
test_features, test_labels, test_keys = load_data_set(TEST_SOURCE);
print(train_keys[0:50]);
print(train_labels[0:50]);
print(test_keys[0:50]);
print(test_labels[0:50]);
                

    
    
###############################
## Train Classifier
###############################
classifier = RandomForestClassifier(n_jobs=NJOBS)
print('Training Classifier...');
classifier.fit(train_features, train_labels)






def generate_predictions(classifier, features, labels, keys):
    max_predictions = (classifier.predict(features));
    predictions = (classifier.predict_proba(features));
    #print(predictions[0:50]);
    print(labels[0:50]);
    print(max_predictions[0:50]);
    print(keys[0:25]);

    classification_df = pd.DataFrame();
    classification_df["is_plant"] = np.array((labels), 'int');
    classification_df["pred_plant"] = max_predictions;
    classification_df["key"] = keys;
    classification_df["pred_0"] = predictions[:, 0];
    classification_df["pred_1"] = predictions[:, 1];
    return classification_df;
def record_predictions(classification_df, delta_mod, split_mod):
    filename = delta_mod;
    file_name = "results/"+filename + '_'+split_mod+'_neg.csv';
    classification_df.sort_values(['pred_0'], ascending=[False], inplace=False).to_csv(file_name, index=False);
    print(file_name + ', done!');
    file_name = "results/"+filename + '_'+split_mod+'_pos.csv';
    classification_df.sort_values(['pred_1'], ascending=[False], inplace=False).to_csv(file_name, index=False);
    print(file_name + ', done!');
#################################
## Classify and record predicitons
#################################
print("\nClassifying test data...");
test_classification = generate_predictions(classifier, test_features, test_labels, test_keys);
record_predictions(test_classification, delta_mod, "test");

print("\nClassifying training data...");
train_classification = generate_predictions(classifier, train_features, train_labels, train_keys);
record_predictions(train_classification, delta_mod, "train");


#################################
## Save Hyperparameter config
#################################
hyperstring = "";
hyperparamlist = ['delta_mod', 'source_mod'];
for name in hyperparamlist:
    name_of_var = name;
    val_of_var = eval(name);
    hyperstring += name_of_var + " : " + str(val_of_var) + "\n";

myfile = open("results/"+delta_mod+"_z_hyperparams.txt", "w+");
myfile.write(hyperstring);
myfile.close();
print("Hyperparameters written.");



#print(preds);
##print(pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds']))