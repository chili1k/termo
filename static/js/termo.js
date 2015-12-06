// SLO date format
$(document).ready(function() {
	$('.termoDate')
	.datepicker({
		weekStart: 1,
		format: 'dd.mm.yyyy',
		language: 'sl'
	})
	.on('changeDate', function(e) {
		// Revalidate the date field
		validateInput();
	});
	$('.termoTime').timepicker({
		minuteStep: 1,
		template: 'modal',
		appendWidgetTo: 'body',
		showSeconds: false,
		showMeridian: false,
		defaultTime: false
	})
	.on("changeTime.timepicker",function(e) {
		validateInput();
	});
});

function pad(number, length) {
	var str = '' + number;
	while (str.length < length) {
		str = '0' + str;
	}
	return str;
}

function getStartDateFull() {
	var startDate = $("#startDate").datepicker("getDate");
	var startTime = $("#startTime").data('timepicker');
	startDate.setHours(startTime.hour);
	startDate.setMinutes(startTime.minute);
	return startDate;
}

function getEndDateFull() {
	var endDate = $("#endDate").datepicker("getDate");
	var endTime = $("#endTime").data('timepicker');
	endDate.setHours(endTime.hour);
	endDate.setMinutes(endTime.minute);
	return endDate;
}

function validateInput() {
	var startDate = getStartDateFull();
	var endDate = getEndDateFull();

	if (endDate.getTime() < startDate.getTime()) {
		$("#rangeValidator").fadeIn(500).css("display","block")
		return false;
	}
	else {
		$("#rangeValidator").css("display","none")
		return true;
	}
}

// Format time as yymmddhhmm
// GetMonth returns 0-11
function formatDate(d) {
	return d.getFullYear().toString()+
				pad((d.getMonth()+1).toString(),2)+pad(d.getDate().toString(),2)+
				pad(d.getHours(),2)+pad(d.getMinutes(),2);
}

$(function() {
	$("#showGraphButton").click(function(){
		validateInput();
		if (validateInput()) {
			var startDate = getStartDateFull();
			var endDate = getEndDateFull();
			var start = formatDate(startDate);
			var end = formatDate(endDate);
			var sensorid = parseInt($("#sensorid").val());
			var graphLink = "/graph?sensorid="+sensorid+"&start="+start+"&end="+end
			$("#graph").fadeOut(100).html($("img").attr("src",graphLink)).fadeIn("slow");
		}
	});
});