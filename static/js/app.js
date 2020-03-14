function buildCharts(state) {
    // TO DO: Iterate through all states

    d3.json(`/metadata/state/${state}`, function(stateData) {
        console.log(state);

        // Cast rates as numbers

        console.log('state data', stateData);
        
        // Build line chart
	    var trace1 = {
            x: stateData.year,
            y: stateData.Prescription_Deaths,
            type: "line",
            text: 'Number of Deaths'
        };
        var data = [trace1];
        var layout = {
            title: `Number of Overdose Deaths in ${state}`,
            xaxis: { title: "Year"},
            yaxis: { title: "Number of Deaths"}
        };
        Plotly.newPlot("line", data, layout);        
    });
    
}

function buildCharts(state) {
    // TO DO: Iterate through all states

    d3.json(`/metadata/state/${state}`, function(stateData) {
        console.log(state);

        // Cast rates as numbers

        console.log('state data', stateData);
        
        // Build line chart
	    var trace1 = {
            x: stateData.year,
            y: stateData.Crude_Rate_Per_100000,
            type: "line",
            text: 'Rate per 100,000'
        };
        var data = [trace1];
        var layout = {
            title: `Death Rate per 100,000 Citizens in ${state}`,
            xaxis: { title: "Year"},
            yaxis: { title: "overdose Rate per 100,000 (%)"}
        };
        Plotly.newPlot("line", data, layout);        
    });
    
}

function buildCharts(state) {
    // TO DO: Iterate through all states

    d3.json(`/metadata/state/${state}`, function(stateData) {
        console.log(state);

        // Cast rates as numbers

        console.log('state data', stateData);
        
        // Build line chart
	    var trace1 = {
            x: stateData.year,
            y: stateData.Prescribing_Rate_Per_100,
            type: "line",
            text: 'Number of Deaths'
        };
        var data = [trace1];
        var layout = {
            title: `Prescription Rate per 100 Citizens in ${state}`,
            xaxis: { title: "Year"},
            yaxis: { title: "Prescription Rate per 100 (%)"}
        };
        Plotly.newPlot("line", data, layout);        
    });
    
}

function init() {      

    // Set up the dropdown menu
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/states").then((state) => {
        state.forEach((instance) => {
        selector
            .append("option")
            .text(instance)
            .property("value", instance);
        });

        // Use Alabama to build the initial plot
        const defaultState = state[0];
        buildCharts(defaultState);
    });
}

function optionChanged(newState) {
    // Fetch new data each time a new state is selected
    buildCharts(newState);
}

init();