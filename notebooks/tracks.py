import gosling as gos

def _create_gene_annotations_track():
    data = gos.beddb(
        url="https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation",
        genomicFields=[{"index": 1, "name": "start"}, {"index": 2, "name": "end"}],
        valueFields=[
            {"index": 5, "name": "strand", "type": "nominal"},
            {"index": 3, "name": "name", "type": "nominal"},
        ],
        exonIntervalFields=[
            {"index": 12, "name": "start"},
            {"index": 13, "name": "end"},
        ],
    )

    base = gos.Track(data)

    text = (
        base.mark_text(dy=-15)
        .encode(
            text="name:N",
            x="start:G",
            xe="end:G",
        )
        .transform_filter(
            field="type",
            oneOf=["gene"],
        )
    )

    plus_end = (
        base.mark_triangleRight()
        .encode(
            x=gos.X("end:G", axis="top"),
            size=gos.value(15),
        )
        .transform_filter(field="type", oneOf=["gene"])
        .transform_filter(field="strand", oneOf=["+"])
    )

    minus_end = (
        base.mark_triangleLeft(align="right")
        .encode(
            x="start:G",
            size=gos.value(15),
        )
        .transform_filter(field="type", oneOf=["gene"])
        .transform_filter(
            field="strand",
            oneOf=["-"],
        )
    )

    exon = (
        base.mark_rect()
        .encode(
            x="start:G",
            xe="end:G",
            size=gos.value(15),
        )
        .transform_filter(
            field="type",
            oneOf=["exon"],
        )
    )

    plus = (
        base.mark_rule(linePattern=dict(type="triangleRight", size=5))
        .encode(
            x="start:G",
            xe="end:G",
            strokeWidth=gos.value(3),
        )
        .transform_filter(
            field="type",
            oneOf=["gene"],
        )
        .transform_filter(
            field="strand",
            oneOf=["+"],
        )
    )

    minus = (
        base.mark_rule(linePattern=dict(type="triangleLeft", size=5))
        .encode(
            x="start:G",
            xe="end:G",
            strokeWidth=gos.value(3),
        )
        .transform_filter(
            field="type",
            oneOf=["gene"],
        )
        .transform_filter(
            field="strand",
            oneOf=["-"],
        )
    )

    return gos.overlay(
        text, plus_end, minus_end, exon, plus, minus
    ).properties(
        row=gos.Row("strand:N", domain=["+", "-"]),
        color=gos.Color("strand:N", domain=["+", "-"], range=["#7585FF", "#FF8A85"]),
        visibility=[
            {
                "operation": "less-than",
                "measure": "width",
                "threshold": "|xe-x|",
                "transitionPadding": 10,
                "target": "mark",
            }
        ],
        opacity=gos.value(0.8),
    )

gene_annotation = _create_gene_annotations_track()
