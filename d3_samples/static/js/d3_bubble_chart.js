// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function d3BubbleChartSample(bubbleContainer, diameter, data, staticURL,
		bubblePadding, bubbleNodeDy, bubbleNodeTextAnchor) {
	var format = d3.format(",d"), color = d3.scale.category20c();

	var bubble = d3.layout.pack().sort(null).size([ diameter, diameter ])
			.padding(bubblePadding);

	var svg = d3.select(bubbleContainer).append("svg").attr("width", diameter)
			.attr("height", diameter).attr("class", "bubble");

	d3.json("/measurements", function(error, measurements) {
		if (error)
			throw error;
		var dataSet = {};
		measurements.measurements.filter(function(d) {
			return d.name == data
		}).forEach(function(root, i, measurements) {
			if (dataSet[root.value] == undefined)
				dataSet[root.value] = 1;
			else
				dataSet[root.value] += 1;
		});

		var root = {
			'children' : []
		}
		for ( var i in dataSet) {
			root['children'].push({
				'name' : i,
				'size' : dataSet[i]
			});
		}
		var node = svg.selectAll(".node").data(
				bubble.nodes(classes(root)).filter(function(d) {
					return !d.children;
				})).enter().append("g").attr("class", "node").attr("transform",
				function(d) {
					return "translate(" + d.x + "," + d.y + ")";
				});

		node.append("title").text(function(d) {
			return d.className + ": " + format(d.value);
		});

		node.append("circle").attr("r", function(d) {
			return d.r;
		}).style("fill", function(d) {
			return color(d.packageName);
		});

		node.append("text").attr("dy", bubbleNodeDy).style("text-anchor",
				bubbleNodeTextAnchor).text(function(d) {
			return d.className.substring(0, d.r / 3);
		});
	});

	function classes(root) {
		var classes = [];

		function recurse(name, node) {
			if (node.children)
				node.children.forEach(function(child) {
					recurse(node.name, child);
				});
			else
				classes.push({
					packageName : name,
					className : node.name,
					value : node.size
				});
		}

		recurse(null, root);
		return {
			children : classes
		};
	}

	d3.select(self.frameElement).style("height", diameter + "px");
}
