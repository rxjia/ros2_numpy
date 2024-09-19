
from .registry import converts_from_numpy

from std_msgs.msg import ColorRGBA
import numpy as np

@converts_from_numpy(ColorRGBA)
def numpy_to_color_rgba(arr):
    assert arr.shape[-1] == 4

    if len(arr.shape) == 1:
        return ColorRGBA(**dict(zip(["r", "g", "b", "a"], arr)))
    else:
        return np.apply_along_axis(
            lambda v: ColorRGBA(**dict(zip(["r", "g", "b", "a"], v))), axis=-1, arr=arr
        )
