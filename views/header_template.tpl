<!DOCTYPE HTML>
<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/css/termo_style.css">
<script src="/static/js/jquery-1.9.0.min.js"></script>
<script src="/static/js/jquery-ui/jquery-ui-1.10.0.custom.min.js"></script>
<script src="/static/js/jquery-ui/jquery.ui.datepicker-sl.js"></script>
<link rel="stylesheet" href="/static/js/jquery-ui/themes/base/jquery-ui.css">
</head>
<body>
	<div id="sideBar">
	<select>
        %for row in sensors:
		<option value="{{row['sensorid']}}">{{row['name']}}</a>
        %end
	</select>

        <ul class="nav">
                <li><a href="/sensor/{{row['sensorid']}}">Nadzorna plošča</a></li>
                <li><a href="/sensor/edit/{{row['sensorid']}}">Nastavitve</a></li>
        </ul>
	</div>

<div id="mainContent">
