
var CSTree = function(config){
	var margin 	= config.margin;
	var width	= config.width - margin.left - margin.right;
	var height 	= config.height - margin.top - margin.bottom;
	var selected = null;
	var i = 0,
    duration = 750,
    root = config.data,
    nodes=null, links=null, filter=config.filter;
    var df = d3.format(".4f");

    var size = d3.scale.linear();
    var fsize = d3.scale.linear();
    var doiLabel = config.useDOILabel;

	var tree = nw.layout.tree()
	.nodeSize([20,180])
	.separation(function(a, b) { return (a.parent == b.parent ? 1 : 2); })
	    //.size([height, width]);

	var diagonal = d3.svg.diagonal()
	    .projection(function(d) { return [d.y, d.x]; });

    var aggregate = d3.svg.symbol()
    	.type("triangle-down")
    	.size(function(d){ return d._children? 8*d._children.length : 0; })

	var svg = d3.select(config.container).append("svg")
	    .attr("width", width + margin.right + margin.left)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	  root.x0 = height / 2;
	  root.y0 = 0;

	function chart(){

	}

	chart.useDOILabel = function(enabled){
		doiLabel = enabled;
	}
  // 	chart.collapse = function (d) {
		// if (d.children) {
		// 	d._children = d.children;
		// 	d._children.forEach(chart.collapse);
		// 	d.children = null;
		// }
  // 	}
  	chart.create = function(){
  		//backup childern
		chart.visit(root, function(d){
			if (d.children) d._children = d.children.slice();
		})
		chart.update(root);
  	}
  	chart.visit = function(node, callback){
	    var nodes = [ node ];
	    while ((node = nodes.pop()) != null) {
	      callback(node);
	      if ((children = node.children) && (n = children.length)) {
	        var n, children;
	        while (--n >= 0) nodes.push(children[n]);
	      }
	    }
  	}
	//d3.select(self.frameElement).style("height", "800px");
	chart.update = function (source) {
  		//restore childern
		chart.visit(root, function(d){
			if (d._children) d.children = d._children.slice();
			d.collapsed = false;
		})
		// Compute the new tree layout.
		nodes = tree.nodes(root).reverse(),
		  	

		nodes.forEach(function(d){//translate to center
			d.x += height/2;
		});
		console.log(nodes.length);
		// Calculate DOI values (TODO: removed 'nodes')
		filter.operate(nodes, root, 5, root.approved)
		var params = filter.getParams();
		var min =  -d3.max(nodes, function(d){ return d.depth+1;});
		min -= params.isLocalOn? 1: 0;
		min -= params.isSocialOn? params.weight*root.visitRatio: 0;
		//Update scale
		size.domain([min, 0])
			.range([2, 10])
		fsize.domain([min, 0])
			.range([8, 14])

		// Iteratively Adjusting Layout
		// sort by doi values
		var sorted = nodes.sort(function(a, b){	return b.doi-a.doi; });
		var h = d3.max(nodes, function(d){ return d.x; }) - d3.min(nodes, function(d){ return d.x; });
		var n;
		while((h > height) && (n = sorted.pop()) ){
			//console.log("height, limit: " +h + ", " + height);
			console.log(n.doi)
			n.filtered = true;
			var idx = n.parent.children.indexOf(n);
			n.parent.children.splice(idx, 1);
			//is collapsed
			if (n.parent.children.length==0){
				n.parent.collapsed = true;
				delete n.parent.children;
			}
			// if ((n.parent.children.length-1)==n.parent._children.length){//only after an element removed first time
			// 	n.parent.children.push{
			// 		name: "2 items",
			// 		doi: n.doi,
			// 		approved: 0,
			// 		parent : n.parent,
			// 		elided : 
			// 	}
			// }
			
			// Compute the new tree layout.
			nodes = tree.nodes(root).reverse(),
			  	

			nodes.forEach(function(d){//translate to center
				d.x += height/2;
			});
			var h = d3.max(nodes, function(d){ return d.x; }) - d3.min(nodes, function(d){ return d.x; });
		}

		links = tree.links(nodes);
		
		

		// Update the nodes…
		var node = svg.selectAll("g.node")
		  	.data(nodes, function(d) { return d.id || (d.id = ++i); });
		node.transition().select("text")	
			.text(function(d) { return doiLabel? df(d.doi) : d.name; });//return d.name + "("+nodes.indexOf(d)+", " +df(d.doi)+")"; })

		// Enter any new nodes at the parent's previous position.
		var nodeEnter = node.enter().append("g")
		  	.attr("class", "node")
		  	//.style("opacity", 1e-6)
		  	.attr("transform", function(d) { return (d.parent && d.parent.y0)? "translate(" + d.parent.y0 + "," + d.parent.x0 + ")": "translate("+root.y+","+root.x+")"; })
		 	.on("click", chart.click)
		 	.on('mouseover', chart.onMouseOver)
	      	.on('mouseout', chart.onMouseOut);;

		nodeEnter.append("circle")
		 	.attr("r", 1e-6)
		  	.style("fill", "#fff");

		nodeEnter.append("text")
			.attr("x", function(d) { return -10; })
			.attr("dy", ".35em")
			.attr("text-anchor", function(d) { return  "end" ; })
			.text(function(d) { return doiLabel? df(d.doi) : d.name; }) //{ return d.name + "("+nodes.indexOf(d)+", " +df(d.doi)+")"; })
			.style("fill-opacity", 1e-6)
			.style("font-size", "0px");

		nodeEnter.append("path")
		 	.attr("transform", function(d) { return "translate(" + 2*size(d.doi) + "," + 0 + ") rotate(90)"; })
			.attr("fill", "gray")
			.style("fill-opacity", 1e-6)
		 	.attr("d", aggregate);


		// Transition nodes to their new position.
		var nodeUpdate = node.transition()
		  	.duration(duration)
		  	//.style("opacity", function(d){ return alpha(d.doi); })
		  	.attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

		nodeUpdate.select("circle")
		  	.attr("r", function(d) { return size(d.doi); })
		  	.style("fill", "#fff");

		nodeUpdate.select("text")
		  	.style("fill-opacity", 1.0)
		  	.style("font-size", function(d) { return fsize(d.doi)+"px";});

	  	
		nodeUpdate.select("path")			
			.style("fill-opacity", function(d){ return d.collapsed? 1.0: 1e-6; })

		// Transition exiting nodes to the parent's new position.
		var nodeExit = node.exit().transition()
		  	.duration(duration)
		  	.attr("transform", function(d) { return d.parent? "translate(" + d.parent.y + "," + d.parent.x + ")": "translate("+root.y+","+root.x+")"; })
		  	.remove();

		nodeExit.select("circle")
		  	.attr("r", 1e-6);

		nodeExit.select("text")
		  	.style("fill-opacity", 1e-6);
		  	
		nodeExit.select("path") 
			.style("fill-opacity", 1e-6);
				
		// Update the links…
		var link = svg.selectAll("path.link")
		  	.data(links, function(d) { return d.target.id; });

		// Enter any new links at the parent's previous position.
		link.enter().insert("path", "g")
		  	.attr("class", "link")
		  	.attr("d", function(d) {
		    	var o = d.source.y0? {x: d.source.x0, y: d.source.y0} : {x:root.x, y:root.y};
		    	return diagonal({source: o, target: o});
		  	});

		// Transition links to their new position.
		link.transition()
		  	.duration(duration)
		  	.attr("d", diagonal);

		// Transition exiting nodes to the parent's new position.
		link.exit().transition()
			.duration(duration)
			.attr("d", function(d) {
				var o = {x: d.source.x, y: d.source.y};
				return diagonal({source: o, target: o});
		  	})
	  	.remove();

		// Stash the old positions for transition.
		nodes.forEach(function(d) {
			d.x0 = d.x;
			d.y0 = d.y;
		});
	}
// Toggle children on click.
	chart.click = function (d) {
		console.log('clicked:' )
		console.log(d)
		// Add a focus node
		if (filter){
			var f = filter.focusNodes();
			if (f.length>0)
				f.pop();
			f.push(d);

		}
		// if (d.children) {
	 //    	d._children = d.children;
	 //    	d.children = null;
	 //  	} else {
	 //    	d.children = d._children;
	 //    	d._children = null;
	 //  	}	
	  	chart.update(root);
	  	//selection
	  	if (selected){//disable highlight	
	  		chart.disableHighlight(selected);		
	  	}
	  	
  		selected = this;
  		chart.enableHighlight(this);
	  	config.onClick.call(this, d);
	}
	chart.onMouseOut = function(d){
		if (this!= selected) chart.disableHighlight(this);
	}
	chart.onMouseOver = function(d){
		if (this!= selected) chart.enableHighlight(this);		
	}
	chart.enableHighlight = function(elem){
		d3.select(elem).select("circle")
			.style("stroke", "orange");
		d3.select(elem).select("text")
			.style("fill", "orange");
	}
	chart.disableHighlight = function(elem){
		d3.select(elem).select("circle")
  			.style("stroke", "steelblue");
		d3.select(elem).select("text")
			.style("fill", "black");
	}
	return chart;
}





