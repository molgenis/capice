import pandas as pd
import numpy as np
import pickle
import argparse
import xgboost as xgb
import gzip

cadd_vars = ['Ref', 'Alt', 'Type', 'Length', 'GC', 'CpG', 'motifECount',
             'motifEScoreChng', 'motifEHIPos',
             'oAA', 'nAA', 'cDNApos', 'relcDNApos', 'CDSpos', 'relCDSpos',
             'protPos', 'relProtPos', 'Domain', 'Dst2Splice',
             'Dst2SplType', 'minDistTSS', 'minDistTSE', 'SIFTcat', 'SIFTval',
             'PolyPhenCat', 'PolyPhenVal', 'priPhCons',
             'mamPhCons', 'verPhCons', 'priPhyloP', 'mamPhyloP', 'verPhyloP',
             'bStatistic', 'targetScan', 'mirSVR-Score',
             'mirSVR-E', 'mirSVR-Aln', 'cHmmTssA', 'cHmmTssAFlnk', 'cHmmTxFlnk',
             'cHmmTx', 'cHmmTxWk', 'cHmmEnhG',
             'cHmmEnh', 'cHmmZnfRpts', 'cHmmHet', 'cHmmTssBiv', 'cHmmBivFlnk',
             'cHmmEnhBiv', 'cHmmReprPC', 'cHmmReprPCWk',
             'cHmmQuies', 'GerpRS', 'GerpRSpval', 'GerpN', 'GerpS', 'TFBS',
             'TFBSPeaks', 'TFBSPeaksMax', 'tOverlapMotifs',
             'motifDist', 'Segway', 'EncH3K27Ac', 'EncH3K4Me1', 'EncH3K4Me3',
             'EncExp', 'EncNucleo', 'EncOCC', 'EncOCCombPVal',
             'EncOCDNasePVal', 'EncOCFairePVal', 'EncOCpolIIPVal',
             'EncOCctcfPVal', 'EncOCmycPVal', 'EncOCDNaseSig',
             'EncOCFaireSig', 'EncOCpolIISig', 'EncOCctcfSig', 'EncOCmycSig',
             'Grantham', 'Dist2Mutation', 'Freq100bp',
             'Rare100bp', 'Sngl100bp', 'Freq1000bp', 'Rare1000bp', 'Sngl1000bp',
             'Freq10000bp', 'Rare10000bp',
             'Sngl10000bp', 'dbscSNV-ada_score', 'dbscSNV-rf_score']

impute_values = {'Ref': 'N', 'Alt': 'N', 'Consequence': 'UNKNOWN', 'GC': 0.42,
                 'CpG': 0.02, 'motifECount': 0,
                 'motifEScoreChng': 0, 'motifEHIPos': 0, 'oAA': 'unknown',
                 'nAA': 'unknown', 'cDNApos': 0,
                 'relcDNApos': 0, 'CDSpos': 0, 'relCDSpos': 0, 'protPos': 0,
                 'relProtPos': 0, 'Domain': 'UD', 'Dst2Splice': 0,
                 'Dst2SplType': 'unknown', 'minDistTSS': 5.5, 'minDistTSE': 5.5,
                 'SIFTcat': 'UD', 'SIFTval': 0,
                 'PolyPhenCat': 'unknown', 'PolyPhenVal': 0, 'priPhCons': 0.115,
                 'mamPhCons': 0.079, 'verPhCons': 0.094,
                 'priPhyloP': -0.033, 'mamPhyloP': -0.038, 'verPhyloP': 0.017,
                 'bStatistic': 800, 'targetScan': 0,
                 'mirSVR-Score': 0, 'mirSVR-E': 0, 'mirSVR-Aln': 0,
                 'cHmmTssA': 0.0667, 'cHmmTssAFlnk': 0.0667,
                 'cHmmTxFlnk': 0.0667, 'cHmmTx': 0.0667, 'cHmmTxWk': 0.0667,
                 'cHmmEnhG': 0.0667, 'cHmmEnh': 0.0667,
                 'cHmmZnfRpts': 0.0667, 'cHmmHet': 0.667, 'cHmmTssBiv': 0.667,
                 'cHmmBivFlnk': 0.0667, 'cHmmEnhBiv': 0.0667,
                 'cHmmReprPC': 0.0667, 'cHmmReprPCWk': 0.0667,
                 'cHmmQuies': 0.0667, 'GerpRS': 0, 'GerpRSpval': 0,
                 'GerpN': 1.91, 'GerpS': -0.2, 'TFBS': 0, 'TFBSPeaks': 0,
                 'TFBSPeaksMax': 0, 'tOverlapMotifs': 0,
                 'motifDist': 0, 'Segway': 'unknown', 'EncH3K27Ac': 0,
                 'EncH3K4Me1': 0, 'EncH3K4Me3': 0, 'EncExp': 0,
                 'EncNucleo': 0, 'EncOCC': 5, 'EncOCCombPVal': 0,
                 'EncOCDNasePVal': 0, 'EncOCFairePVal': 0,
                 'EncOCpolIIPVal': 0, 'EncOCctcfPVal': 0, 'EncOCmycPVal': 0,
                 'EncOCDNaseSig': 0, 'EncOCFaireSig': 0,
                 'EncOCpolIISig': 0, 'EncOCctcfSig': 0, 'EncOCmycSig': 0,
                 'Grantham': 0, 'Dist2Mutation': 0,
                 'Freq100bp': 0, 'Rare100bp': 0, 'Sngl100bp': 0,
                 'Freq1000bp': 0, 'Rare1000bp': 0, 'Sngl1000bp': 0,
                 'Freq10000bp': 0, 'Rare10000bp': 0, 'Sngl10000bp': 0,
                 'dbscSNV-ada_score': 0,
                 'dbscSNV-rf_score': 0}


def examine_nas(df):
    sample_num = df.shape[0]
    null_ratios = {}
    for col in df.columns:
        null_number = df[col].isnull().sum()
        if null_number > 0:
            null_ratios[col] = null_number / sample_num
            print(col, null_number, round(null_number / sample_num, 2))
    return null_ratios


def replace_nas(df, Dict):
    for value in df.columns:
        if df[value].isna().any() and value in Dict:
            df[value].fillna(impute_values[value], inplace=True)
        else:
            continue
    return df


def impute(df, imputed_savepath=None):
    print(type(df))
    print("Readin data shape: ", df.shape)
    print(df.head())
    df = df.dropna(subset=cadd_vars, how="all")
    print("Remove samples with no parameters, shape: ", df.shape)
    func = lambda x: np.nan if pd.isnull(x) or x == "." else float(x)
    values = df["dbscSNV-rf_score"].values
    df["dbscSNV-rf_score"] = [func(item) for item in values]
    df = df.dropna(how="all")
    print("Raw data loaded, shape: ", df.shape)
    print("Before imputation, null ratio: \n")
    _ = examine_nas(df[cadd_vars])
    # save null ratios
    df = replace_nas(df, impute_values)
    print("After imputation, there shouldn't be any nulls, but check below: \n")
    _ = examine_nas(df)
    if imputed_savepath:
        df.to_csv(imputed_savepath, index=False)
        print("Saved imputed raw file to %s" % imputed_savepath)
    return df


def return_top10_or_less_categories(a_column, return_num=10):
    value_counts = a_column.value_counts()
    if len(value_counts) > return_num:
        print(value_counts.index[:return_num].values)
        return value_counts.index[:return_num].values
    else:
        print(value_counts.index.values)
        return value_counts.index.values


def process_categoricalvars(data, feat_cadd_object, isTrain=False,
                            catFeats_levels_dict=None, catFeatNames_dict=None):
    if isTrain:
        print("Determining feature levels from the training dataset.")
        for catFeat in catFeats_levels_dict.keys():
            featNames = return_top10_or_less_categories(data[catFeat],
                                                        return_num=
                                                        catFeats_levels_dict[
                                                            catFeat])
            print(
                "For feature %s, saved %d levels." % (catFeat, len(featNames)))
            data[catFeat] = np.where(data[catFeat].isin(featNames),
                                     data[catFeat], "other")
    else:
        print("Using features from the trained model.")
        for catFeat in catFeatNames_dict.keys():
            featNames = catFeatNames_dict[catFeat]
            print(
                "For feature %s, saved %d levels." % (catFeat, len(featNames)))
            data[catFeat] = np.where(data[catFeat].isin(featNames),
                                     data[catFeat], "other")
    data = pd.get_dummies(data, columns=feat_cadd_object)
    return data


def preprocess(imputed_data, processed_savepath=None, isTrain=False,
               model_path=None, model_features=None):
    print("\n\n\n\n\n\n\n", isTrain)
    feat_cadd_object = [feat for feat in
                        imputed_data.select_dtypes(include=["O"]).columns
                        if feat in cadd_vars]
    print("Categorical variables", len(feat_cadd_object))
    num_samples = imputed_data.shape[0]
    print("In total, there are %d samples" % num_samples)
    catFeats_levels_dict = {"Ref": 5, "Alt": 5, "Domain": 5}
    if isTrain:
        print("\n\n\n\n\n\n\nPre-processing using training procedures")
        for feat in feat_cadd_object:
            if feat not in catFeats_levels_dict:
                catFeats_levels_dict[feat] = 5
        processed_data = process_categoricalvars(imputed_data,
                                                 feat_cadd_object=feat_cadd_object,
                                                 isTrain=isTrain,
                                                 catFeats_levels_dict=catFeats_levels_dict)
    else:
        print("\n\n\n\n\n\n\nPre-processing using model features")
        if model_path:
            # Since I don't know at what version they deprecated feature names
            if int(xgb.__version__.split('.')[0]) < 1:
                model_features = pickle.load(
                    open(model_path, 'rb')).feature_names
            else:
                # Very much illegal to access a private class in python
                # (marked by _Class)
                model_features = pickle.load(
                    open(model_path, 'rb'))._Booster.feature_names
        elif model_features:
            model_features = model_features
        else:
            print(
                "In testing phase, features needs to be specified "
                "or pretrained models needs to be provided...")
        catFeatNames_dict = {}
        for feature in feat_cadd_object:
            for feature_expandedname in model_features:
                if feature in feature_expandedname:
                    expandedname = '_'.join(feature_expandedname.split('_')[1:])
                    if feature in catFeatNames_dict:
                        catFeatNames_dict[feature].append(expandedname)
                    else:
                        catFeatNames_dict[feature] = [expandedname]
        processed_data = process_categoricalvars(imputed_data,
                                                 feat_cadd_object=feat_cadd_object,
                                                 isTrain=isTrain,
                                                 catFeatNames_dict=catFeatNames_dict)
        for col in model_features:
            if col not in processed_data:
                processed_data[col] = 0
                print("Feature from the model not in data: ", col)
    print(processed_data[model_features].shape)
    if processed_savepath:
        print("Saving preprocessed data to ", processed_savepath)
        processed_data.to_csv(processed_savepath, index=False)
    return processed_data


def make_predictions(preprocessed_data, prediction_savepath, model_path):
    model = pickle.load(open(model_path, "rb"))
    # Since I don't know at what version they deprecated feature names
    if int(xgb.__version__.split('.')[0]) < 1:
        model_features = model.feature_names
        input_matrix = xgb.DMatrix(preprocessed_data[model_features])
        preprocessed_data['probabilities'] = model.predict(input_matrix)
        pathogenicity = 0.152
    else:
        # Very much illegal to access a private class in python
        # (marked by _Class)
        model_features = model._Booster.feature_names
        input_matrix = preprocessed_data[model_features]
        preprocessed_data['probabilities'] = model.predict_proba(
            input_matrix)[:, 1]
        pathogenicity = 0.02
    preprocessed_data['ID'] = '.'
    tellPathogenic_prediction = lambda \
        x: "Pathogenic" if x > pathogenicity else "Neutral"
    preprocessed_data['prediction'] = [tellPathogenic_prediction(probability)
                                       for probability
                                       in preprocessed_data['probabilities']]
    tellPathogenic_combinedPrediction = lambda x: \
        "Pathogenic" if x[0] > 0.02 or x[1] > 30 else "Neutral"
    preprocessed_data['combined_prediction'] = [
        tellPathogenic_combinedPrediction(probability) for probability
        in preprocessed_data[['probabilities', 'PHRED']].values]
    save_columns = ['chr_pos_ref_alt', 'GeneName', 'Consequence', 'PHRED',
                    'probabilities', 'prediction', 'combined_prediction']
    save_file = preprocessed_data[save_columns]
    save_file = save_file.sort_values("probabilities",
                                      ascending=False).drop_duplicates(
        'chr_pos_ref_alt')
    save_file.to_csv(prediction_savepath, sep="\t", index=False)
    print("Prediction file saved in ", prediction_savepath)
    print(save_file.head())
    return save_file


def check_input_columns(input_path):
    print("Reading CADD output file from :", input_path)
    skip_rows = 0
    for line in gzip.open(input_path):
        if line.decode().startswith('##CADD'):
            skip_rows = 1
        break
    input = pd.read_csv(input_path, sep="\t", skiprows=skip_rows,
                        compression="gzip")
    print(input.head())
    print("CADD output file loaded. File shape:", input.shape)
    for column in cadd_vars:
        if column not in input:
            raise IOError("Please annotate the file by CADD first.")
    input['chr_pos_ref_alt'] = ['_'.join([str(ele) for ele in item]) for item
                                in
                                input[['#Chrom', 'Pos', 'Ref', 'Alt']].values]
    return input


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", dest="input_path", type=str)
    parser.add_argument("--imputed_savepath", dest="imputed_savepath", type=str)
    parser.add_argument("--processed_savepath", dest="processed_savepath",
                        type=str)
    parser.add_argument("--isTrain", dest='isTrain', type=bool)
    parser.add_argument("--model_path", dest="model_path", type=str)
    parser.add_argument("--prediction_savepath", dest='prediction_savepath',
                        type=str)
    parser.add_argument("--log_path", dest='log_path', type=str)
    args = parser.parse_args()

    # sys.stdout = open("%s"%args.log_path, "w")
    print("Input file is:", args.input_path)
    if args.isTrain == 'True':
        isTrain = True
    else:
        isTrain = False
    input = check_input_columns(args.input_path)
    preprocessed_data = preprocess(imputed_data=impute(input), isTrain=isTrain,
                                   model_path=args.model_path)
    _ = make_predictions(preprocessed_data, args.prediction_savepath,
                         args.model_path)
    # sys.stdout.close()
