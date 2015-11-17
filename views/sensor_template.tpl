%include header_template sensors=sensors
%import datetime

<div id="sensorData">
	<fieldset>
	<table>
		<tr><td>Notranja temperatura:</td><td><strong>{{round(sensor['temperature'],1)}} <sup>o</sup>C</strong></td></tr>
		<tr><td>Zunanja temperatura:</td><td><strong>{{outsidetemp}} <sup>o</sup>C</strong></td></tr>
		<tr><td>Stanje gretja:</td><td class='{{'ON' if relaystate else 'OFF'}}'><strong>{{'Vklopljeno' if relaystate else 'Izklopljeno'}}</strong></td></tr>
	</table>
	</fieldset>

	<form action="/relay/toggle/{{sensor['relayid']}}" method="get">
		<input type="hidden" id="sensorid" name="sensorid" value="{{sensor['sensorid']}}">
		<input class="button" type="submit" id="sensorAction" name="sensorAction" value="{{'Izklopi gretje' if sensor['relaystate'] else 'Vklopi gretje'}}">
	</form>

	<div id="sensorGraph">
		<p class="graphTitle">Graf notranje temperature:</p>
		<fieldset id="graphPeriod" class=>
			<label for="startDate">Od:</label>
			<input type="text" id="startDate" name="startDate" class="dateInput datePicker" 
				value="{{starttime.strftime('%d.%m.%Y')}}">
			<input type="text" id="startTime" name="startTime" class="timeInput" 
				value="{{starttime.strftime('%H:%M')}}">
			<label for="endDate">Do:</label>
                        <input type="text" id="endDate" name="endDate" class="dateInput datePicker"
				value="{{endtime.strftime('%d.%m.%Y')}}">
                        <input type="text" id="endTime" name="endTime" class="timeInput"
				value="{{endtime.strftime('%H:%M')}}">
		</fieldset>

		<input class="button" type="button" id="showGraph" name="dateAction" value="Prikaži">
		<p><img class="graph" src="{{!sensorgraph}}"></p>
		<p class="graphSubtitle">Zadnji datum meritve:&nbsp;{{datetime.datetime.strptime(sensor['updatetime'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S, %d.%m.%Y')}}</p>
	</div>
</div>

<script>
$(function() {
$.datepicker.setDefaults( $.datepicker.regional[ "sl" ] );
$( ".datePicker" ).datepicker();

$("#showGraph").click(function(){
	var startDate = $("#startDate").datepicker("getDate");
	var endDate = $("#endDate").datepicker("getDate");
	var startTime = $("#startTime").val();
	var endTime = $("#endTime").val();
	var start = $.datepicker.formatDate('yymmdd',startDate)+startTime.replace(":","");
	var end = $.datepicker.formatDate('yymmdd',endDate)+endTime.replace(":","");
	var sensorid = {{sensor['sensorid']}};
	var graphLink = "/graph?sensorid="+sensorid+"&start="+start+"&end="+end
	$(".graph").fadeOut(100).html($("img").attr("src",graphLink)).fadeIn("slow");
	/*$.get(
	    "/graph?sensorid="+sensorid+"&start="+start+"&end="+end,
	    "",
	    function(data) { ; },
	    "html"
	);*/
});

});
</script>

%include footer_template
