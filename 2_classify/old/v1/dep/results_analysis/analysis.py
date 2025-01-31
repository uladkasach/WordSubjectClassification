import sys
import numpy as np;


def main(delta_mod, offset = '', write_offset = 'results_analysis/'):
    HYPERPARAM_SOURCE =  offset+'results/'+delta_mod+'_z_hyperparams.txt';
    RESULTS_SOURCE =     offset+'results/'+delta_mod+'_freq.csv';
    RESULTS_POS_SOURCE = offset+'results/'+delta_mod+'_pos.csv';
    RESULTS_NEG_SOURCE = offset+'results/'+delta_mod+'_neg.csv';
    TRUE_LABELS_SOURCE = offset+'../../features/label_words/plant_words.txt';
    FREQUENCIES_SOURCE = offset+"inputs/5.6m_basic_freq_table.csv";
    TRAIN_SOURCE = offset+'results/'+delta_mod+'_trainprog.csv';

    #######################################
    ## Load True Labels
    #######################################
    true_words = [];
    f = open(TRUE_LABELS_SOURCE, 'r');
    for line in f.readlines():
        parts = line.rstrip().split(",");
        #print(parts);
        word = parts[0];
        true_words.append(word);
    f.close();
    #print(len(true_words));




    #######################################
    ## Load Frequent Words
    #######################################
    frequency_dict = dict();
    f = open(FREQUENCIES_SOURCE, 'r');
    for line in f.readlines():
        parts = line.rstrip().split(",");
        #print(parts);
        word = parts[0];
        freq = int(parts[1]);
        frequency_dict[word] = freq;
    f.close();

    def parse_results_from(results_source):
        TP = [];
        TN = [];
        FP = [];
        FN = [];
        f = open(results_source, 'r');
        i = -1;
        for line in f.readlines():
            i += 1;
            if(i == 0):
                continue;
            parts = line.rstrip().split(",");
            #print(parts);
            pred_y = int(parts[0]);
            word = parts[1];
            if(pred_y == 0):
                confidence = parts[2];
            else:
                confidence = parts[3];
            confidence = float(confidence);
            freq = frequency_dict[word];
            true_y = 1 if word in true_words else 0;

            data = [true_y, pred_y, word, freq, confidence];
            #print(data);

            #if(i == 200):
            #    exit();

            if(true_y == pred_y):
                if(true_y == 1):
                    TP.append(data);
                else:
                    TN.append(data);
            else:
                if(true_y == 1):
                    FN.append(data);
                else:
                    FP.append(data);
        f.close();
        return TP, TN, FP, FN;

    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()

    print("Reading Hyperparameters...");
    #######################################
    ## Read hyperparam data
    #######################################
    hyperparameter_data = file_get_contents(HYPERPARAM_SOURCE);
    data_string = hyperparameter_data + "\n";

    print("Parsing Results...");
    #######################################
    ## Parse General Results
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_SOURCE);
    print("Writing Stats...");
    data_string += ("TP:" + str(len(TP)) + "\nTN:" +  str(len(TN)) + "\nFP:" + str(len(FP)) + "\nFN:" + str(len(FN)) + "\n");
    data_string += ("%FP:" + str(len(FP)/(len(TN)+len(FP))) + "\n%TP:" +  str(len(TP)/(len(TP)+len(FN))));
    #%F P = F P/(T N +F P )
    #%T P = T P/(T P +F N )

    #######################################
    ## Write FP Results, In order of decreasing Positive Confidence
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_POS_SOURCE);
    print ("Writing FP");
    data_string += "\n---- FP ----\n";
    for data in FP:
        data_string += str(data[0]) + "," + str(data[1]) + "," + data[2] + "," + str(data[3]) + "," + str(data[4]) + "\n";



    #######################################
    ## Write FP Results, In order of decreasing Negative Confidence
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_NEG_SOURCE);
    print ("Writing FN");
    data_string += "\n---- FN ----\n";
    for data in FN:
        data_string += str(data[0]) + "," + str(data[1]) + "," + data[2] + "," + str(data[3]) + "," + str(data[4]) + "\n";



    #######################################
    ## Write TP Results, In order of decreasing Positive Confidence
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_POS_SOURCE);
    print ("Writing TP");
    data_string += "\n---- TP ----\n";
    for data in TP:
        data_string += str(data[0]) + "," + str(data[1]) + "," + data[2] + "," + str(data[3]) + "," + str(data[4]) + "\n";


    print("Reading Training Progress...");
    #######################################
    ## Read hyperparam data
    #######################################
    data_string += "\n---- Train Prog ----\n";
    progress_data = file_get_contents(TRAIN_SOURCE);
    data_string += progress_data + "\n";


    myfile = open(write_offset+"results/"+delta_mod+"_result.csv", "w+");
    myfile.write(data_string);
    myfile.close();


    
if __name__ == "__main__":
    #delta_mod = "PW1";
    delta_mod = sys.argv[1];
    main(delta_mod, '../', '');