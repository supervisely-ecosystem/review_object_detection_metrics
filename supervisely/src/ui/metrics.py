import supervisely as sly
import numpy as np
import globals as g
import confusion_matrix
import per_image_metrics
import per_class_metrics
import overall_metrics
import sys
sys.path.append('../../')
from src.evaluators.pascal_voc_evaluator import get_pascalvoc_metrics
from src.utils.enumerators import MethodAveragePrecision


@sly.timeit
def init(data, state, reconstruct=False):
    state['collapsed5'] = True
    state['disabled5'] = True

    state['activeFigure'] = None
    confusion_matrix.init(data, state)
    per_image_metrics.init(data, state)
    per_class_metrics.init(data, state)
    overall_metrics.init(data, state)
    if reconstruct:
        g.my_app.compile_template(g.root_source_dir)




def dict2tuple(dictionary, target_class, round_level=4):
    false_positive, true__positive, num__positives = 0, 0, 0
    if target_class and target_class != 'ALL':
        dict__ = dictionary['per_class'][target_class]
        false_positive = dict__['total FP']
        true__positive = dict__['total TP']
        num__positives = dict__['total positives']
        average_precision = round(dict__['AP'], round_level)
        recall = round(true__positive / num__positives, round_level) if num__positives != 0 else 0
        precision = round(np.divide(true__positive, (false_positive + true__positive)), round_level) \
            if false_positive + true__positive != 0 else 0
    else:
        try:
            for dict_ in dictionary['per_class']:
                dict__ = dictionary['per_class'][dict_]
                false_positive += dict__['total FP']
                true__positive += dict__['total TP']
                num__positives += dict__['total positives']
        except:
            return g.result(0, 0, 0, 0, 0, 0)
        average_precision = round(dictionary['mAP'], round_level)
        recall = round(true__positive / num__positives, round_level) if num__positives != 0 else 0
        precision = round(np.divide(true__positive, (false_positive + true__positive)), round_level) \
            if false_positive + true__positive != 0 else 0

    return g.result(str(int(true__positive)), str(int(false_positive)), str(int(num__positives)),
                  str(recall), str(precision), str(average_precision))


def calculate_mAP(img_gts_bbs, img_det_bbs, iou, score,
                  method=MethodAveragePrecision.EVERY_POINT_INTERPOLATION) -> list:
    score_filtered_detections = []
    for bbox in img_det_bbs:
        try:
            if bbox.get_confidence() >= score:
                score_filtered_detections.append(bbox)
        except:
            print(bbox)
            if bbox.get_confidence() >= score:
                score_filtered_detections.append(bbox)
    return get_pascalvoc_metrics(img_gts_bbs, score_filtered_detections, iou, generate_table=True, method=method)


def calculate_image_mAP(src_list, dst_list, method, target_class=None, iou=0.5, score=0.01,
                        need_rez=False, show_logs=False):
    images_pd_data = list()
    full_logs = list()
    matched = 0
    print('target_class =', target_class)
    for dataset_name in src_list:
        for src_image_info in src_list[dataset_name]:
            for dst_image_info in dst_list[dataset_name]:
                if src_image_info[1] == dst_image_info[1]:
                    matched += 1
                    rez = calculate_mAP(src_image_info[-1], dst_image_info[-1], iou, score, method)
                    try:
                        rez_d = dict2tuple(rez, target_class)
                        src_image_image_id = src_image_info[0]
                        dst_image_image_id = dst_image_info[0]
                        src_image_image_name = src_image_info[1]
                        src_image_link = src_image_info[2]
                        dataset_name = src_image_info[3]
                        per_image_data = [str(src_image_image_id), str(dst_image_image_id), dataset_name,
                                          '<a href="{0}" rel="noopener noreferrer" target="_blank">{1}</a>'.format(
                                              src_image_link,
                                              src_image_image_name)]
                        per_image_data.extend(rez_d)
                        images_pd_data.append(per_image_data)
                        full_logs.append(rez)
                    except:
                        pass
    if show_logs:
        print('Lengths of sets =', len(src_list), len(dst_list))
        print('processed  {} of (src={}, dst={})'.format(matched, len(src_list), len(dst_list)))
    if need_rez:
        return images_pd_data, full_logs
    else:
        return images_pd_data


def calculate_dataset_mAP(src_dict, dst_dict, method, target_class=None, iou=0.5, score=0.01):
    datasets_pd_data = list()
    dataset_results = []
    # key_list = list(set([el[-2] for el in src_dict]))
    key_list = src_dict.keys()

    for dataset_key in key_list:
        src_set_list = []
        [src_set_list.extend(el[-1]) for el in src_dict[dataset_key] if el[-2] == dataset_key]
        dst_set_list = []
        [dst_set_list.extend(el[-1]) for el in dst_dict[dataset_key] if el[-2] == dataset_key]

        rez = calculate_mAP(src_set_list, dst_set_list, iou, score, method)

        rez_d = dict2tuple(rez, target_class)
        current_data = [dataset_key]
        current_data.extend(rez_d)
        if rez is not None:
            dataset_results.append(rez['per_class'])
        else:
            raise ValueError("Unable to calculate mAP score. You can increase sample size or select other classes.")
        datasets_pd_data.append(current_data)
    return datasets_pd_data


def calculate_project_mAP(src_list, dst_list, method, dst_project_name, target_class=None, iou=0.5, score=0.01):
    projects_pd_data = list()
    src_set_list = []
    # [src_set_list.extend(el[-1]) for el in src_list.values()]
    dst_set_list = []
    # [dst_set_list.extend(el[-1]) for el in dst_list.values()]

    key_list = src_list.keys()
    for dataset_key in key_list:
        [src_set_list.extend(el[-1]) for el in src_list[dataset_key]]
        [dst_set_list.extend(el[-1]) for el in dst_list[dataset_key]]

    prj_rez = calculate_mAP(src_set_list, dst_set_list, iou, score, method)
    rez_d = dict2tuple(prj_rez, target_class)
    current_data = [dst_project_name]
    current_data.extend(rez_d)
    projects_pd_data.append(current_data)
    return projects_pd_data, prj_rez


def line_chart_builder(prj_viz_data, round_level=4):
    line_chart_series = []
    table_classes = []

    for classId, res in prj_viz_data.items():
        if res is None:
            raise IOError(f'Error: Class {classId} could not be found.')
        precision = res['precision']
        recall = res['recall']
        fp = res['total FP']
        tp = res['total TP']
        npos = res['total positives']
        ap = round(res['AP'], round_level)
        # precision recall interpolation is removed: info - see src_backup/algorithm.py
        line_chart_series.append(dict(name=classId, data=[[i, j] for i, j in zip(recall, precision)]))
        recall = round(tp / npos, round_level) if npos != 0 else 0
        precision = round(np.divide(tp, (fp + tp)), round_level) if fp + tp != 0 else 0
        table_classes.append([classId, float(tp), float(fp), float(npos), float(recall), float(precision), float(ap)])
    return line_chart_series, table_classes
