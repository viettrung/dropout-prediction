import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.evaluation.Evaluation;
import weka.core.Instances;
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

		/*String[] options = new String[2];
		options[0] = "-R";
		options[1] = "first-last";

		NumericToNominal filter = new NumericToNominal();
		filter.setOptions(options);
		filter.setInputFormat(data);*/

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
		Evaluation eval = new Evaluation(crossValData);
		for (int n = 0; n < folds; n++) {
			Instances train = crossValData.trainCV(folds, n);
			Instances test = crossValData.testCV(folds, n);

			// build and evaluate classifier
			Classifier clsNaive = new NaiveBayes();
			clsNaive.buildClassifier(train);
			eval.evaluateModel(clsNaive, test);
		}

		// output evaluation
		System.out.println();
		System.out.println("=== Setup ===");
		System.out.println("Dataset: " + data.relationName());
		System.out.println(eval.toSummaryString());
		System.out.println(eval.toClassDetailsString());
		System.out.println(eval.toMatrixString());
	}
}
