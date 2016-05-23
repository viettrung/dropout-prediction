import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.functions.LibSVM;
import weka.classifiers.functions.VotedPerceptron;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Discretize;

/*
 Decision Tree	-> J48
 K-nearest neighbor	-> iBK
 Generalized Linear Regression -> LinearRegession
 Naive Bayes	->  Naive Bayes
 SVM	 -> LibSVM
 Neural Network -> Multilayer Perceptron (VotedPerceptron)
 */

public class Classification {

	public static void main(String[] args) throws Exception {
		DataSource source = new DataSource("Y1_formated.arff");
		Instances data = source.getDataSet();
		// setting class attribute if the data format does not provide this
		// information
		if (data.classIndex() == -1)
			data.setClassIndex(4);

		// filter
		// Remove rm = new Remove();
		// rm.setAttributeIndices("1"); // remove 1st attribute: roll number
		// remove.setInputFormat(data);
		// data = Filter.useFilter(data, rm);

		String[] options = new String[6];
		options[0] = "-B";
		options[1] = "10";
		options[2] = "-M";
		options[3] = "-1.0";
		options[4] = "-R";
		options[5] = "first-last";

		Discretize filter = new Discretize();
		filter.setOptions(options);
		filter.setInputFormat(data);

		/*
		 * String[] options = new String[2]; options[0] = "-R"; options[1] =
		 * "first-last";
		 * 
		 * NumericToNominal filter = new NumericToNominal();
		 * filter.setOptions(options); filter.setInputFormat(data);
		 */

		Instances filterData = Filter.useFilter(data, filter);

		int folds = 10;
		int seed = 1;
		// randomize data
		Random rand = new Random(seed);
		Instances crossValData = new Instances(filterData);
		crossValData.randomize(rand);
		if (crossValData.classAttribute().isNominal())
			crossValData.stratify(folds);

		// perform cross-validation
		Evaluation evalNaiveBayes = new Evaluation(crossValData);
		Evaluation evalSVM = new Evaluation(crossValData);
		Evaluation evalNeuronNetwork = new Evaluation(crossValData);
		
		Evaluation evalDecisionTree = new Evaluation(crossValData);
		Evaluation evalIBK = new Evaluation(crossValData);
		Evaluation evalLR = new Evaluation(crossValData);
		
		for (int n = 0; n < folds; n++) {
			Instances train = crossValData.trainCV(folds, n);
			Instances test = crossValData.testCV(folds, n);

			// build and evaluate classifier
			// naive bayes
			Classifier clsNaive = new NaiveBayes();
			clsNaive.buildClassifier(train);
			evalNaiveBayes.evaluateModel(clsNaive, test);

			// SVM
			LibSVM clsSVM = new LibSVM();
			clsSVM.setOptions(Utils
					.splitOptions("-S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 "
							+ "-model \"C:\\Program Files\\Weka-3-8\" -seed 1"));
			clsSVM.buildClassifier(train);
			evalSVM.evaluateModel(clsSVM, test);

			// Neuron Network
			// MultilayerPerceptron mlp = new MultilayerPerceptron();
			// // L = Learning Rate
			// // M = Momentum
			// // N = Training Time or Epochs
			// // H = Hidden Layers //
			// mlp.setOptions(Utils
			// .splitOptions("-L 0.1 -M 0.2 -N 2000 -V 0 -S 0 -E 20 -H 3"));
			// mlp.buildClassifier(train);
			// evalNeuronNetwork.evaluateModel(mlp, test);
			VotedPerceptron vp = new VotedPerceptron();
			vp.setOptions(Utils.splitOptions("-I 1 -E 1.0 -S 1 -M 10000"));
			vp.buildClassifier(train);
			evalNeuronNetwork.evaluateModel(vp, test);
			
			//Decision Tree
			J48 j48 = new J48();
			j48.setOptions(Utils.splitOptions("-C 0.25 -M 2"));
			j48.buildClassifier(train);
			evalDecisionTree.evaluateModel(j48, test);
			
			//K-nearest neighbor
			IBk ibk = new IBk();
			ibk.setOptions(Utils.splitOptions("-K 1 -W 0"));
			LinearNNSearch linearSearch = new LinearNNSearch(train);
			EuclideanDistance euclideanDistance = new EuclideanDistance(train);
			euclideanDistance.setOptions(Utils.splitOptions("-R first-last"));
			linearSearch.setDistanceFunction(euclideanDistance);
			ibk.setNearestNeighbourSearchAlgorithm(linearSearch);
			ibk.buildClassifier(train);
			evalIBK.evaluateModel(ibk, test);
			
			//Generalized Linear Regression
			Logistic logistic = new Logistic();
			logistic.setOptions(Utils.splitOptions("-R 1.0E-8 -M -1 -num-decimal-places 4"));
			logistic.buildClassifier(train);
			evalLR.evaluateModel(logistic, test);
		}

		// output evaluation
		System.out.println();
		System.out.println("=== Setup ===");
		System.out.println("Dataset: " + data.relationName());
		System.out.println("=== Eval NaiveBayes ===");
		System.out.println(evalNaiveBayes.toSummaryString());
		System.out.println(evalNaiveBayes.toClassDetailsString());
		System.out.println(evalNaiveBayes.toMatrixString());
		System.out.println("=== Eval SVM ===");
		System.out.println(evalSVM.toSummaryString());
		System.out.println(evalSVM.toClassDetailsString());
		System.out.println(evalSVM.toMatrixString());
		System.out.println("=== Neuron Network ===");
		System.out.println(evalNeuronNetwork.toSummaryString());
		System.out.println(evalNeuronNetwork.toClassDetailsString());
		System.out.println(evalNeuronNetwork.toMatrixString());
		System.out.println("=== Decision Tree ===");
		System.out.println(evalDecisionTree.toSummaryString());
		System.out.println(evalDecisionTree.toClassDetailsString());
		System.out.println(evalDecisionTree.toMatrixString());
		System.out.println("=== K-nearest neighbor ===");
		System.out.println(evalIBK.toSummaryString());
		System.out.println(evalIBK.toClassDetailsString());
		System.out.println(evalIBK.toMatrixString());
		System.out.println("=== Generalized Linear Regression ===");
		System.out.println(evalLR.toSummaryString());
		System.out.println(evalLR.toClassDetailsString());
		System.out.println(evalLR.toMatrixString());
	}
}
