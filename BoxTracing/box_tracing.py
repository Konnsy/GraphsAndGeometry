import numpy as np
import sys
from box_tracing_helper import boxIoU, mergeBoxes, isBoxContained, mergeBoxesByIoU, calcCliques

class BoxTracer:
	"""
	Stores a list of boxes for each frame and calculates a list of traces on demand.
	Each trace is of the format (frame list, boxes list) with same length for both lists per trace.
	Each box has to be given in the format [x1, y1, x2, y2].

	Example usage:
		> bbt = BoxTracer(minLenTraces=2, iouThreshold=0.1, distTolerance=2) # see __init__ for explanations 
		> b1 = [0,0,1,1]
		> b2 = [2,2,3,3]
		> bbt.addToTraces([]) # frame 1 has no detection
		> bbt.addToTraces([b1,b2]) # frame 2 has two boxes
		> bbt.addToTraces([b1])
		> bbt.addToTraces([])
		> bbt.addToTraces([b2])
		=> len(bbt.calculateTraces()) will return 2
	"""
	def __init__(self, 
			  minLenTraces=10, 
			  iouThreshold=0.1, 
			  distTolerance=0):
		"""
		minLenTraces: Sort out all traces that are shorter than this 
		iouThreshold: Minimum iou two must have to be merged into one trace
		distTolerance: The max. size of the gap between two boxes that are still merged into one.
						This can bridge short times of missing detections 
						when there are occurences before and after the gap.
		                
		"""
		self.boxesPerFrame = []
		self.iou_thresh = iouThreshold
		self.min_trace_len = minLenTraces
		self.dist_tol = distTolerance
		self.distance_tolerance = distTolerance


	def addToTraces(self, boxes):
		"""
		Adds a list of boxes for a frame. The frame count is increased automatically. 
		If no boxes are to add for a frame, just add an empty list.
		"""
		self.boxesPerFrame.append(mergeBoxesByIoU(boxes, self.iou_thresh))


	def calculateTraces(self):
		"""
		Returns a list of traces from the added boxes where each trace is a pair (list of frames, list of boxes).
		The length of both lists is equal per frame.
		"""
		traces = []
		bbPerTrace = {} # bounding box per trace

		traceIdsByFrame = {}
		for frame in range(len(self.boxesPerFrame)):
			traceIdsByFrame[frame] = []

		# create a trace for each box in the first frame
		for box in self.boxesPerFrame[0]:
			traces.append([[0], [box]])
			traceIdsByFrame[0].append(len(traces)-1)
			bbPerTrace[len(traces)-1] = box

		for frame_idx in range(1, len(self.boxesPerFrame)):			
			for box in self.boxesPerFrame[frame_idx]:
				boxAdded = False
				
				# select existent trace to search in
				# (looking 1 + distance tolerance steps backward)
				trace_ids = []
				for dt in range(self.dist_tol+1):
					idx_check = frame_idx-1-dt
					if idx_check >= 0 :
						for trace_id_check in traceIdsByFrame[idx_check]:
							if len(traces[trace_id_check]) > 0:
								trace_ids.append(trace_id_check)

				for trace_idx in trace_ids:
					# check intersection with the bounding box of the trace
					traceBoundingBox = bbPerTrace[trace_idx]
					if (boxIoU(box, traceBoundingBox) >= self.iou_thresh
						or isBoxContained(box, traceBoundingBox)):
						traces[trace_idx][0].append(frame_idx)						
						traces[trace_idx][1].append(box)
						traceIdsByFrame[frame_idx].append(trace_idx)
						bbPerTrace[trace_idx] = mergeBoxes([bbPerTrace[trace_idx], box])
						boxAdded = True
						break
			
				# open new trace if box was not added to an existing one
				if not boxAdded:
					traces.append([[frame_idx], [box]])
					traceIdsByFrame[frame_idx].append(len(traces)-1)
					bbPerTrace[len(traces)-1] = box
			
		# sort out traces that are too short
		# the length is defined by max_frame - min_frame + 1
		traces = list(filter(lambda t : t[0][-1] - t[0][0] + 1 >= self.min_trace_len, traces))
		return traces
		
