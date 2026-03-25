window.rocketSplitTest.convertActiveTests = function() {
	var activeTests = [];
	for (var i = 0; i < window.rocketSplitTest.tests.length; i++) {
		var test = window.rocketSplitTest.tests[i];
		for (var k = 0; k < test.variations.length; k++) {
			var variation = test.variations[k];
			if (variation.active) {
				activeTests.push({
					'testId': test.id,
					'variationId': variation.id
				});
			}
		}
	}
	return activeTests;
};

window.rocketSplitTest.getConversions = function () {
	var conversions = [];
	for (var i = 0; i < window.rocketSplitTest.conversion.testIds.length; i++) {
		var testId = window.rocketSplitTest.conversion.testIds[i];
		var cookieName = "elementor_split_test_" + testId + "_variation";
		var cookieValue = window.rocketSplitTest.cookie.read(cookieName);
		if (cookieValue != null) {
			conversions.push({
				'testId': testId,
				'variationId': cookieValue
			});
		}
	}
	return conversions;
};

window.rocketSplitTest.ajax = {};
window.rocketSplitTest.ajax.post = function(path, data, callback) {
	var urlBase = window.rocketSplitTest.config.page.base;
	path = path.charAt(0) === "/" ? path.substr(1) : path;
	var	xhr = new XMLHttpRequest();
	xhr.open('POST', urlBase.protocol + urlBase.host + urlBase.path + path + "?rnd=" + Math.floor(Math.random() * 1000000000000));
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function () {
		if (xhr.readyState !== 4) {
			return;
		}
		if (xhr.status >= 200 && xhr.status < 300) {
			if (typeof callback !== 'undefined' && callback != null) {
				callback(JSON.parse(xhr.responseText));
			}
		}
	};
	xhr.send(encodeURI(data));
};

var views = 'views=' + JSON.stringify(window.rocketSplitTest.convertActiveTests());
window.rocketSplitTest.ajax.post('/wp-json/splitTestForElementor/v1/tracking/view/store-multi/', views, function (data) {
	console.log(data);
	window.rocketSplitTest.cookie.create('elementor_split_test_client_id', data.clientId, 365);
});

var conversions = 'conversions=' + JSON.stringify(window.rocketSplitTest.getConversions());
window.rocketSplitTest.ajax.post('/wp-json/splitTestForElementor/v1/tracking/conversion/store-multi/', conversions, null);