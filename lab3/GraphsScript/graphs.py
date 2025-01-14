import matplotlib.pyplot as plt

from measurement import Measurement


def get_axis_data(data: dict, x_label: str, y_label: str):
    cases = set()
    for m_dict in data:
        cases.add(m_dict[Measurement.CASE_TAG])
    axis = {}
    case_tag = Measurement.CASE_TAG
    for case in cases:
        axis[case] = {}
        x_points = [m[x_label] for m in data if m[case_tag] == case]
        y_points = [m[y_label] for m in data if m[case_tag] == case]
        axis[case]["x_points"] = x_points
        axis[case]["y_points"] = y_points
    return axis


def graph(
    measurements,
    x_tag,
    y_tag,
    x_label,
    y_label,
    graph_title,
    xlambda=None,
    ylambda=None
):
    axis = get_axis_data(
        [m.to_dictionary() for m in measurements],
        x_tag,
        y_tag
    )
    fig, ax = plt.subplots()
    for case in axis:
        print(f"y points for case {case}: {axis[case]['y_points']}")
        x_points = axis[case]["x_points"]
        y_points = axis[case]["y_points"]

        if (xlambda is not None):
            x_points = list(map(xlambda, x_points))

        if (ylambda is not None):
            y_points = list(map(ylambda, y_points))

        ax.plot(x_points, y_points, label=case)
    plt.style.use("ggplot")
    plt.legend()
    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def graph_measurements(measurements: list[Measurement]):
    graph_useful_load_curve(measurements)
    graph_delay_curve(measurements)
    graph_network_overload(measurements)


def graph_useful_load_curve(measurements: list[Measurement]):
    x_tag = Measurement.GENRATE_TAG
    y_tag = Measurement.RECRATE_TAG
    x_label = "Carga ofrecida [pkt/seg]"
    y_label = "Carga útil [pkt/seg]"
    title = "Carga Útil vs Ofrecida"
    graph(measurements, x_tag, y_tag, x_label, y_label, title)


def graph_network_overload(measurements):
    x_tag = Measurement.GENRATE_TAG
    y_tag = Measurement.TOTALDROP_TAG
    x_label = "Paquetes generados [pkt/seg]"
    y_label = "Pérdida de paquetes"
    title = "Índice de pérdida de paquetes"
    graph(measurements, x_tag, y_tag, x_label, y_label, title)


def graph_delay_curve(measurements: list[Measurement]):
    x_tag = Measurement.GENRATE_TAG
    y_tag = Measurement.AVDEL_TAG
    x_label = "Carga ofrecida [pkt/seg]"
    y_label = "Retraso promedio [s]"
    title = "Retraso"
    graph(measurements, x_tag, y_tag, x_label, y_label, title)