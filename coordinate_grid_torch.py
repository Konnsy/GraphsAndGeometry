import torch

def coordinateGrid2D(numX, numY):
    x = torch.arange(numX)
    y = torch.arange(numY)
    grid_x, grid_y = torch.meshgrid(x,y)
    return torch.stack([grid_x, grid_y], dim=2)