import numpy
from PIL import Image
from pathlib import Path


def evaluation(expected: Path, actual: Path):
    """
    Return the Intersection over Union (IoU), Precision, Recall, and F1 Scores
    Expected and actual bit masks should be the same dimensions
    """
    expected_im = Image.open(expected)
    actual_im = Image.open(actual)

    # Converts images to single channel gray-scale
    expected_im = expected_im.convert("L")
    actual_im = actual_im.convert("L")

    e_array = numpy.array(expected_im)
    a_array = numpy.array(actual_im)

    assert expected_im.size == actual_im.size

    width, height = e_array.shape

    union_count = 0
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for w in range(width):
        for h in range(height):
            union_count += 1 if e_array[w][h] or a_array[w][h] else 0

            true_positive += 1 if e_array[w][h] and a_array[w][h] else 0
            true_negative += 1 if not e_array[w][h] and not a_array[w][h] else 0
            false_positive += 1 if not e_array[w][h] and a_array[w][h] else 0
            false_negative += 1 if e_array[w][h] and not a_array[w][h] else 0

    iou = 0 if union_count == 0 else true_positive / union_count
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = (2 * precision * recall) / (precision + recall)

    return iou, precision, recall, f1_score
