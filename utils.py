import numpy
from PIL import Image
from pathlib import Path


def evaluation(expected: Path, actual: Path):
    """
    Return the Accuracy, Precision, Recall, and F1 Scores
    Expected and actual bit masks should be the same dimensions
    """
    expected_im = Image.open(expected)
    actual_im = Image.open(actual)

    # Converts images to single channel gray-scale
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
