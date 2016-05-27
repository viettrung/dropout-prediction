import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class ArtifactClassification {

	public static void main(String[] args) throws Exception {
		DataSource source = new DataSource("Y1_formated.arff");
		Instances data = source.getDataSet();

		data.randomize(new java.util.Random(0));

		int trainSize = (int) Math.round(data.numInstances() * 0.8);
		int testSize = data.numInstances() - trainSize;
		Instances trainData = new Instances(data, 0, trainSize);
		Instances testData = new Instances(data, trainSize, testSize);

		System.out.print("Data size: " + data.size());
		System.out.print("\nTrain size: " + trainData.size());
		System.out.print("\nTest size: " + testData.size());
	}
}
