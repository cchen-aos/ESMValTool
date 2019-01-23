#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Diagnostic script to create multiple MLR models for many climate models.

Description
-----------
This diagnostic creates multiple "Machine Learning Regression" (MLR) models to
predict future climate for several climate models.

Author
------
Manuel Schlund (DLR, Germany)

Project
-------
CRESCENDO

Configuration options in recipe
-------------------------------
See esmvaltool.mlr module.

"""

import logging
import os

from esmvaltool.diag_scripts.mlr import MLRModel
from esmvaltool.diag_scripts.shared import (group_metadata, run_diagnostic,
                                            select_metadata)

logger = logging.getLogger(os.path.basename(__file__))


def main(cfg):
    """Run the diagnostic."""
    input_data = cfg['input_data'].values()
    preselection = cfg.get('metadata_preselection', {})
    group = preselection.get('group')
    input_data = select_metadata(input_data, **preselection.get('select', {}))
    grouped_datasets = group_metadata(input_data, group)
    for attr in grouped_datasets:
        logger.info("Processing %s", attr)
        if group is not None:
            metadata = {group: attr}
        else:
            metadata = {}
        mlr_model = MLRModel(cfg, root_dir=attr, **metadata)

        # Fit and predict
        mlr_model.simple_train_test_split()
        mlr_model.export_training_data()
        mlr_model.fit()
        mlr_model.predict()

        # Plots
        mlr_model.plot_scatterplots()
        mlr_model.plot_feature_importance()
        mlr_model.plot_partial_dependences()
        mlr_model.plot_prediction_error()


# Run main function when this script is called
if __name__ == '__main__':
    with run_diagnostic() as config:
        main(config)