%include header_template sensors=sensors,activepage=activepage
%import datetime

<div id="heatingContainer" class="container text-center">
	<div class="alert {{'alert-warning' if sensor['relaystate'] else 'alert-info'}}">
	 	<h4>Stanje gretja: <strong>{{'Vklopljeno' if relaystate else 'Izklopljeno'}}</strong></h4>
		<div>
		<form action="/relay/toggle/{{sensor['relayid']}}" method="get">
			<input type="hidden" id="sensorid" name="sensorid" value="{{sensor['sensorid']}}">
			<button id="sensorAction" name="sensorAction" type="submit" class="btn btn-warning">
				<span class="glyphicon glyphicon-off"></span> {{'Izklopi gretje' if sensor['relaystate'] else 'Vklopi gretje'}}
			</button>
		</form>
		</div>
	</div>
</div>

<ul id="temperaturePanel" class="nav navbar-nav navbar-right">
        <li class="text-muted">
        	Notranja temperatura: <span class="label label-primary">{{round(sensor['temperature'],1)}} <sup>o</sup>C</span>
        </li>
		<li class="text-muted">
			Zunanja temperatura: <span class="label label-info">{{outsidetemp}} <sup>o</sup>C</span>
		</li>
</ul>

<div id="historyContainer" class="container">
<hr>
	<div id="historyPanel" class="panel panel-default">
		<div class="panel-heading">Zgodovina meritev</div>
		<div class="panel-body">
			<form class="form-inline dateForm" role="form">
				 <div class="form-group">
				 	<label for="startDate">Začetek:</label>
					<input type="text" id="startDate" name="startDate" class="form-control termoDate" value="{{starttime.strftime('%d.%m.%Y')}}">
				</div>
				 <div class="form-group">
					<input type="text" id="startTime" class="form-control termoTime" value="{{starttime.strftime('%H:%M')}}">
				</div>
				<div class="form-group">
				 	<label for="endDate">Konec:</label>
					<input type="text" id="endDate" name="endDate" class="form-control termoDate" value="{{endtime.strftime('%d.%m.%Y')}}">
				</div>
				 <div class="form-group">
					<input type="text" id="endTime" class="form-control termoTime" value="{{endtime.strftime('%H:%M')}}">
				</div>
			</form>

			<button id="showGraphButton" type="button" class="btn btn-primary">Prikaži</button>
		</div>	
	</div>	
	<div id="rangeValidator" class="alert alert-warning">
		<strong>Napaka!</strong> Začetni datum mora biti manjši od končega datuma!
	</div>

	<br>
	<div id="lastReadingBlock">
		<div>
			<img id="graph" src="{{!sensorgraph}}">
			<p style="text-align:right"><span class="label label-default">Datum zadnje meritve: {{datetime.datetime.strptime(sensor['updatetime'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S, %d.%m.%Y')}}</span></p>
		</div>
	</div>
</div> <!-- /container -->

%include footer_template
