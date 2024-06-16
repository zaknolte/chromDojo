from dash import Dash, dcc, html, Input, Output, State, ALL, Patch, callback, MATCH
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# base peak accordion - no peaks exist by default
annotations_accordian = dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl(
                    "Annotation Options",
                    icon=DashIconify(
                        icon="quill:label",
                        color="black",
                        width=20,
                    ),
                ),
                dmc.AccordionPanel(
                    [
                        dag.AgGrid(
                            id="annotations-options",
                            columnDefs=[
                                {
                                    "field": "Field",
                                    "width": 140,
                                    "resizable": False,
                                    "sortable": False,
                                    "suppressMovable": True,
                                    "rowDrag": True,
                                },
                                {
                                    "field": "Add to Plot",
                                    "width": 140,
                                    "resizable": False,
                                    "sortable": False,
                                    "suppressMovable": True,
                                    "cellRenderer": "Checkbox",
                                    "cellStyle": {"textAlign": "center"}
                                },
                            ],
                            rowData=[
                                {"Field": "Peak Name", "Add to Plot": False},
                                {"Field": "RT", "Add to Plot": False},
                                {"Field": "Concentration", "Add to Plot": False},
                                {"Field": "Area", "Add to Plot": False},
                                {"Field": "Height", "Add to Plot": False},
                            ],
                            dashGridOptions={
                                "domLayout": "autoHeight",
                                "animateRows": True,
                                "rowDragManaged": True,
                                "suppressCellFocus": True
                                },
                            # columnSize="sizeToFit",
                            style={"width": 300, "height": None},
                            className="ag-theme-balham-dark"
                        )
                    ],
                    id="add-annotation-accordian"
                ),
            ],
            value="annotation-accordian",
        ),
    ]
)