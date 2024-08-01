import numpy
import matplotlib.pyplot as plt     # for the graph
from PIL import Image
import PIL.ImageOps                 # not quite sure why this is here, tbh WAIT I REMEMBER it's to flip the deepforest masks
from pathlib import Path

def evaluation(expected: Path, actual: Path):
    """
    Return the Accuracy, Precision, Recall, and F1 Scores
    Expected and actual bit masks should be the same dimensions
    """
    expected_im = Image.open(expected)
    actual_im = Image.open(actual)

    # Converts images to single channel gray-scale
    # expected_im = PIL.ImageOps.invert(expected_im.convert("L"))
    expected_im = expected_im.convert("L")
    actual_im = actual_im.convert("L")

    expected = numpy.array(expected_im)
    actual = numpy.array(actual_im)

    assert expected_im.size == actual_im.size

    width, height = expected.shape

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for w in range(width):
        for h in range(height):
            true_positive += 1 if expected[w][h] and actual[w][h] else 0
            true_negative += 1 if not expected[w][h] and not actual[w][h] else 0
            false_positive += 1 if not expected[w][h] and actual[w][h] else 0
            false_negative += 1 if expected[w][h] and not actual[w][h] else 0

    accuracy = (true_positive + true_negative) / (width * height)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = (2 * precision * recall) / (precision + recall)

    return accuracy, precision, recall, f1_score

# lists created to store evaluation metrics
# items list is for the naming convention (look at the lines for expected_mask and actual_mask)

item_list = ['1a', '1b', '1c', '1d', '2a', '2b', '2c', '2d', '3a', '3b', '3c', '3d', '4a', '4b', '4c', '4d']
accuracy_list = []
precision_list = []
recall_list = []
f1_list = []

# this section calculates accuracy, precision, recall, and f1 score for all 16 parts of the image
# it also creates a graph using matplotlib
# make sure you include the masks to be compared in the same folder as this program
# alternatively, provide it with the path to the masks

if __name__ == "__main__":
    for item in item_list:
        expected_mask = 'boxmask'+item+'.png'           # names each ground truth mask
        actual_mask = 'predictionboxmask'+item+'.png'   # names each predicted mask
        item_acc, item_prec, item_rec, item_f1 = evaluation(expected_mask, actual_mask)
        accuracy_list.append(round(item_acc,3))
        precision_list.append(round(item_prec,3))
        recall_list.append(round(item_rec,3))
        f1_list.append(round(item_f1,3))
    
    average_accuracy = sum(accuracy_list)/len(accuracy_list)
    average_precision = sum(precision_list)/len(precision_list)
    average_recall = sum(recall_list)/len(recall_list)
    average_f1 = sum(f1_list)/len(f1_list)

    print(f'Accuracy List: {accuracy_list}')
    print(f'Precision List: {precision_list}')
    print(f'Recall List: {recall_list}')
    print(f'F1 Score List: {f1_list}')
    print('')
    print(f'Average Accuracy: {average_accuracy}')
    print(f'Average Precision: {average_precision}')
    print(f'Average Recall: {average_recall}')
    print(f'Average F1 Score: {average_f1}')
    print('')

    data = [accuracy_list, precision_list, recall_list, f1_list]
    # Create a box plot
    plt.figure(figsize=(10, 7))  # Set the figure size
    plt.boxplot(data, vert=True, patch_artist=True, labels=['Accuracy', 'Precision', 'Recall', 'F1 Score'])
    
    # Add titles and labels
    plt.title('Model Evaluation Metrics - DeepForest')
    plt.xlabel('Metrics')
    plt.ylabel('Values')

    # Optional: add a grid
    plt.grid(True)
    plt.ylim(0, 1) # Set the limits for y-axis (min, max)

    # Show the plot
    plt.show()

    # Save the plot to a file
    plt.savefig('box_whisker_plot.png')