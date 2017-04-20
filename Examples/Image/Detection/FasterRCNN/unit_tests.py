import os, sys
from cntk import input as input_variable, user_function

abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path)
sys.path.append(os.path.join(abs_path, "..", ".."))
sys.path.append(os.path.join(abs_path, "lib"))
sys.path.append(os.path.join(abs_path, "lib", "rpn"))
sys.path.append(os.path.join(abs_path, "lib", "nms"))
sys.path.append(os.path.join(abs_path, "lib", "nms", "gpu"))

import pytest
import numpy as np
from lib.rpn.proposal_layer import ProposalLayer as CntkProposalLayer
from lib.rpn.proposal_layer_caffe import ProposalLayer as CaffeProposalLayer

def test_dummy():
    im_info = [1000, 1000, 1]

    bg_probs = [0.2, 0.05, 0.05, 0.0, 0.0, 0.1, 0.1, 0.0, 0.5]
    fg_probs = np.ones(9) - bg_probs
    cls_prob = np.zeros((61, 61, 9, 2))
    cls_prob[:, :, :, 0] = bg_probs
    cls_prob[:, :, :, 1] = fg_probs
    cls_prob = np.ascontiguousarray(cls_prob.transpose(3, 2, 1, 0)).astype(np.float32)

    bbox_pred = [0.2, -0.1, 0.3, -0.4] * 9
    rpn_bbox_pred = np.zeros((61, 61, 36))
    rpn_bbox_pred[:, :, :] = bbox_pred
    rpn_bbox_pred = np.ascontiguousarray(rpn_bbox_pred.transpose(2, 1, 0)).astype(np.float32)

    cls_prob_var = input_variable((2,9,61,61))
    rpn_bbox_var = input_variable((36,61,61))

    cntk_layer = user_function(CntkProposalLayer(cls_prob_var, rpn_bbox_var, im_info=im_info))
    state, cntk_output = cntk_layer.forward({cls_prob_var: [cls_prob], rpn_bbox_var: [rpn_bbox_pred]})
    cntk_proposals = cntk_output[next(iter(cntk_output))][0]

    cls_prob_caffe = cls_prob.reshape((18,61,61))
    bottom = [np.array([cls_prob_caffe]),np.array([rpn_bbox_pred]),np.array([im_info])]
    top = None # handled through return statement in caffe layer for unit testing

    caffe_layer = CaffeProposalLayer()
    caffe_layer.setup(bottom, top)
    caffe_output = caffe_layer.forward(bottom, top)
    caffe_proposals = caffe_output[:,1:]

    assert cntk_proposals.shape == caffe_proposals.shape
    assert np.allclose(cntk_proposals, caffe_proposals, rtol=0.0, atol=0.0)

if __name__ == '__main__':
    test_dummy()