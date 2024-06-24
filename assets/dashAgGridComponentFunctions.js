// custom component to display boolean data as a checkbox

var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.Checkbox = function (props) {
    const {setData, data} = props;

    function onClick() {
        if (!('checked' in event.target)) {
            const checked = !event.target.children[0].checked;
            const colId = props.column.colId;
            props.node.setDataValue(colId, checked);
        }
    };

    function checkedHandler() {
        // update grid data
        const checked = event.target.checked;
        const colId = props.column.colId;
        props.node.setDataValue(colId, checked);
        // update cellRendererData prop so it can be used to trigger a callback
        setData(checked);
    };

    return React.createElement(
        'div',
        {onClick: onClick},
        React.createElement('input', {
            type: 'checkbox',
            checked: props.value,
            onChange: checkedHandler,
            style: {cursor: 'pointer'},
        })
    );
};


dagcomponentfuncs.deleteCal = function (props) {
    const {setData, data} = props;

    function onClick() {
        setData(props.value)
    }

    let iconify = React.createElement(window.dash_iconify.DashIconify, {icon: props.icon});

    return React.createElement(
        window.dash_mantine_components.Button,
        {
            onClick,
            variant: props.variant,
            color: props.color,
            iconify,
        },
        props.value
    );
};