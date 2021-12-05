import pandas as pd
import numpy as np
import plotly.graph_objects as go



def _sliding_chunker(original, segment_len, slide_len):
    #
    """Split a list into a series of sub-lists...
    each sub-list window_len long,
    sliding along by slide_len each time. If the list doesn't have enough
    elements for the final sub-list to be window_len long, the remaining data
    will be dropped.
    e.g. sliding_chunker(range(6), window_len=3, slide_len=2)
    gives [ [0, 1, 2], [2, 3, 4] ]
    """
    #
    chunks = []
    for pos in range(0, len(original), slide_len):
        chunk = np.copy(original[pos : pos + segment_len])
        if len(chunk) != segment_len:
            continue
        chunks.append(chunk)
    return chunks


def _clean_chunks(original, modified, segment_len):
    #
    """appends the output argument to fill in the gaps from incomplete chunks"""
    results = []
    results = modified + [False] * (len(original) - len(modified))
    # set every value in a qualified chunk to True
    for i in reversed(range(len(results))):
        if results[i]:
            for d in range(segment_len):
                results[i + d] = True
    return results


def apply_rules(original, rules="all"):
    mean = original.mean()
    sigma = original.std()
    if rules == "all":
        rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]
    df = pd.DataFrame(original)
    for i in range(len(rules)):
        df[rules[i].__name__] = rules[i](original, mean, sigma)

    return df


def rule1(original, mean=None, sigma=None):
    """One point is more than 3 standard deviations from the mean."""
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    copy_original = original
    ulim = mean + (sigma * 3)
    llim = mean - (sigma * 3)
    results = []
    for i in range(len(copy_original)):
        if copy_original[i] < llim:
            results.append(True)
        elif copy_original[i] > ulim:
            results.append(True)
        else:
            results.append(False)
    return results


def rule2(original, mean=None, sigma=None):
    """Nine (or more) points in a row are on the same side of the mean."""
    if mean is None:

        mean = original.mean()
    if sigma is None:

        sigma = original.std()
    copy_original = original
    segment_len = 9
    side_of_mean = []
    for i in range(len(copy_original)):
        if copy_original[i] > mean:
            side_of_mean.append(1)
        else:
            side_of_mean.append(-1)
    chunks = _sliding_chunker(side_of_mean, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        if chunks[i].sum() == segment_len or chunks[i].sum() == (-1 * segment_len):
            results.append(True)
        else:
            results.append(False)
    # clean up results
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def rule3(original, mean=None, sigma=None):
    """Six (or more) points in a row are continually increasing (or decreasing)."""
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    segment_len = 6
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        chunk = []
        # Test the direction with the first two data points and then iterate from there.
        if chunks[i][0] < chunks[i][1]:  # Increasing direction
            for d in range(len(chunks[i]) - 1):
                if chunks[i][d] < chunks[i][d + 1]:
                    chunk.append(1)
        else:  # decreasing direction
            for d in range(len(chunks[i]) - 1):
                if chunks[i][d] > chunks[i][d + 1]:
                    chunk.append(1)
        if sum(chunk) == segment_len - 1:
            results.append(True)
        else:
            results.append(False)
    # clean up results
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def rule4(original, mean=None, sigma=None):
    """Fourteen (or more) points in a row alternate in direction, increasing then decreasing."""
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    segment_len = 14
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        current_state = 0
        result = False
        for d in range(len(chunks[i]) - 1):
            # direction = int()
            if chunks[i][d] < chunks[i][d + 1]:
                direction = -1
            else:
                direction = 1
            if current_state != direction:
                current_state = direction
                result = True
            else:
                result = False
                break
        results.append(result)
    # fill incomplete chunks with False
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def rule5(original, mean=None, sigma=None):
    """Two (or three) out of three points in a row are more than 2 standard deviations
    from the mean in the same direction."""
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    segment_len = 2
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        if all(i > (mean + sigma * 2) for i in chunks[i]) or all(
            i < (mean - sigma * 2) for i in chunks[i]
        ):
            results.append(True)
        else:
            results.append(False)
    # fill incomplete chunks with False
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def rule6(original, mean=None, sigma=None):
    """Four (or five) out of five points in a row are more than 1 standard deviation
    from the mean in the same

    direction."""
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    segment_len = 4
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        if all(i > (mean + sigma) for i in chunks[i]) or all(
            i < (mean - sigma) for i in chunks[i]
        ):
            results.append(True)
        else:
            results.append(False)
    # fill incomplete chunks with False
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def rule7(original, mean=None, sigma=None):
    """Fifteen points in a row are all within 1 standard deviation of the mean on either side of the mean.
    """
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    segment_len = 15
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        if all((mean - sigma) < i < (mean + sigma) for i in chunks[i]):
            results.append(True)
        else:
            results.append(False)
    # fill incomplete chunks with False
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def rule8(original, mean=None, sigma=None):
    """Eight points in a row exist, but none within 1 standard deviation of the mean,
    and the points are in both directions from the mean.
    """
    if mean is None:
        mean = original.mean()
    if sigma is None:
        sigma = original.std()
    segment_len = 8
    copy_original = original
    chunks = _sliding_chunker(copy_original, segment_len, 1)
    results = []
    for i in range(len(chunks)):
        if (
            all(i < (mean - sigma) or i > (mean + sigma) for i in chunks[i])
            and any(i < (mean - sigma) for i in chunks[i])
            and any(i > (mean + sigma) for i in chunks[i])
        ):
            results.append(True)
        else:
            results.append(False)
    # fill incomplete chunks with False
    results = _clean_chunks(copy_original, results, segment_len)
    return results


def info_SPCrules(data):
    if data == 1:
        #
        print("One point is more than 3 standard deviations from the mean")
        #
    if data == 2:
        print("Nine (or more) points in a row are on the same side of the mean.")
        #
    if data == 3:
        print("Six (or more) points in a row are continually increasing (or decreasing).")
        #
    if data == 4:
        print(
            "Fourteen (or more) points in a row alternate in direction, increasing then decreasing."
        )
        #
    if data == 5:
        print(
            """Two (or three) out of three points in a row are
            more than 2 standard deviations from the mean in the same direction."""
        )
    if data == 6:
        print(
            """Four (or five) out of five points in a row are more than
            1 standard deviation from the mean in the same direction."""
        )
        #
    if data == 7:
        print(
            """Fifteen points in a row are all within 1 standard deviation
            of the mean on either side of the mean."""
        )
        #
    if data == 8:
        print(
            """Eight points in a row exist, but none within 1 standard deviation of the mean,
            and the points are in both directions from the mean."""
        )


def control_chart(data, y_name, xlabel = None, title = "Controlchart", lsl = None, usl = None, outlier = True, lines= True, mean = None, sigma = None):

    if mean == None:
        mean_data = np.nanmean(data[y_name])
    else:
        mean_data = mean
    if sigma == None:
        std_data = np.nanstd(data[y_name])
    
    if xlabel is not None: 
        if isinstance(data[xlabel], pd.Series):
            label_list = data[xlabel].tolist()
            label_list = [str(i) for i in label_list]
            label_val = list(data.index)
        else:
            label_list = None
            label_val = None

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data[y_name], mode='markers', name=y_name))

    if lines: 
        fig.add_hline(y=mean_data, line = dict(color="blue"))
        fig.add_hline(y=mean_data+std_data, line_dash="dot")
        fig.add_hline(y=mean_data-std_data, line_dash="dot")
        fig.add_hline(y=mean_data+2*std_data, line_dash="dot")
        fig.add_hline(y=mean_data-2*std_data, line_dash="dot")
        fig.add_hline(y=mean_data+3*std_data, line = dict(color="red"))
        fig.add_hline(y=mean_data-3*std_data, line = dict(color="red"))

    if lsl:
        fig.add_hline(y=lsl, line = dict(color="orange"))

        lsl_data = data[data[y_name] <= lsl]
        lsl_data

        fig.add_trace(go.Scatter(x=lsl_data.index, y=lsl_data[y_name], mode='markers', name="below lsl", marker = dict(
                size = 6, color = "red" )))
    
    if usl:

        fig.add_hline(y=usl, line = dict(color="orange"))

        usl_data = data[data[y_name] >= usl]
        usl_data
        fig.add_trace(go.Scatter(x=usl_data.index, y=usl_data[y_name], mode='markers', name="above usl", marker = dict(
                size = 6, color = "red" )))

    if outlier:

        data1 = data.loc[rule1(original=data[y_name]), y_name]
        data2 = data.loc[rule2(original=data[y_name]), y_name]
        data3 = data.loc[rule3(original=data[y_name]), y_name]
        data4 = data.loc[rule4(original=data[y_name]), y_name]
        data5 = data.loc[rule5(original=data[y_name]), y_name]
        data6 = data.loc[rule6(original=data[y_name]), y_name]
        data7 = data.loc[rule7(original=data[y_name]), y_name]
        data8 = data.loc[rule8(original=data[y_name]), y_name]

        fig.add_trace(go.Scatter(x=data1.index, y=data1, mode='markers', name="rule1"))
        fig.add_trace(go.Scatter(x=data2.index, y=data2, mode='markers', name="rule2"))
        fig.add_trace(go.Scatter(x=data3.index, y=data3, mode='markers', name="rule3"))
        fig.add_trace(go.Scatter(x=data4.index, y=data4, mode='markers', name="rule4"))
        fig.add_trace(go.Scatter(x=data5.index, y=data5, mode='markers', name="rule5"))
        fig.add_trace(go.Scatter(x=data6.index, y=data6, mode='markers', name="rule6"))
        fig.add_trace(go.Scatter(x=data7.index, y=data7, mode='markers', name="rule7"))
        fig.add_trace(go.Scatter(x=data8.index, y=data8, mode='markers', name="rule8"))

    if xlabel is not None:
        fig.update_xaxes(
                ticktext = label_list,
                tickvals = label_val
                )

    fig.update_layout(
        title=title)

    fig.show()


