import torch
import torch.nn as nn
import warnings

def getDistanceGridTensor(shape, center, device, norm=True, elliptic=False, invert=False):
    """
    Get a grid of the given shape containing the distance of each point 
    to the given center as a scalar value
    """
    shape = (shape[1], shape[0])
    xOrig, yOrig = shape

    if elliptic:
        shape = [max(xOrig, yOrig), max(xOrig, yOrig)]
        relPos = (center[1]/xOrig, center[0]/yOrig)
        center = (relPos[0]*shape[0], relPos[1]*shape[1])

    # create a grid containing distances to the center    
    s1 = torch.arange(shape[1], device=device).repeat(shape[0]).view(shape[0], -1)
    s2 = torch.arange(shape[0], device=device).repeat_interleave(shape[1]).view(shape[0], -1)

    grid = torch.stack([s1, s2], 0)
    distances = torch.sqrt(((grid[0] - center[0])**2) + ((grid[1] - center[1])**2))

    if elliptic:
        distances = distances.view(1,1,distances.shape[-2], distances.shape[-1])

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            distances = nn.functional.interpolate(
                distances,
                size=(xOrig, yOrig),
                mode='bilinear', 
                align_corners=None,
                recompute_scale_factor=None)

    distances = distances.float()

    if norm:
        distances = distances / torch.max(distances)

    if invert:
        distances = torch.max(distances)-distances

    return distances