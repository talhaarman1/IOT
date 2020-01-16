
var username = "";
var password = "";
$(document).ready(function(){
	username = getCookie("username");
	password = getCookie("password");
	if (username != "") {
        toastr.success("Welcome again " + username);
    } else {
        location.href = "login.html";
    }
	var width = $( window ).width();
	var height = $( window ).height();
	
	if(width < 640){
		$("#streamimg").width(width - 60);
	}
});

function LedOn(){
	CallControlApi("lighton");
}
function LedOff(){
	CallControlApi("lightoff");
}
function Forward(){
	CallControlApi("forward");
}
function Left(){
	CallControlApi("left");
}
function Brake(){
	CallControlApi("brake");
}
function Right(){
	CallControlApi("right");
}
function Reverse(){
	CallControlApi("reverse");
}
function HornOn(){
	CallControlApi("hornon");
}
function HornOff(){
	CallControlApi("hornoff");
}
function FanOn(){
	CallControlApi("fanon");
}
function FanOff(){
	CallControlApi("fanoff");
}

function Angle0(){
	CallMovementApi(0);
	}

function Angle45(){
	CallMovementApi(45);
	}
function Angle90(){
	CallMovementApi(90);
	}
function Angle135(){
	CallMovementApi(135);
	}
	
function Angle180(){
	CallMovementApi(180);
	}
function FrontSensor(){
	$.ajax({
			type: "GET",
			url: baseuri + "/api/" + "frontsensor",
			dataType: "json",
			headers: {
				"Authorization": "Basic " + btoa(username + ":" + password)
			},
			success: function (data){
					$("#response").prepend(JSON.stringify(data) + '</br>');
					toastr.success(data.reading + " cms", 'IOT Robot Sensor');
			},
			error: function(xhr, status, error) {
				toastr.error("Status: " + status + " Error: " + error, "Oops!");
			}
	});
}
function Humidity(){
	$.ajax({
			type: "GET",
			url: baseuri + "/api/" + "humidity",
			dataType: "json",
			headers: {
				"Authorization": "Basic " + btoa(username + ":" + password)
			},
			success: function (data){
					$("#response").prepend(JSON.stringify(data) + '</br>');
					toastr.success(data.reading + " cms", 'IOT Robot Sensor');
			},
			error: function(xhr, status, error) {
				toastr.error("Status: " + status + " Error: " + error, "Oops!");
			}
	});
}
function Temperature(){
	$.ajax({
			type: "GET",
			url: baseuri + "/api/" + "temperature",
			dataType: "json",
			headers: {
				"Authorization": "Basic " + btoa(username + ":" + password)
			},
			success: function (data){
					$("#response").prepend(JSON.stringify(data) + '</br>');
					toastr.success(data.reading + " cms", 'IOT Robot Sensor');
			},
			error: function(xhr, status, error) {
				toastr.error("Status: " + status + " Error: " + error, "Oops!");
			}
	});
}



function AllSideSensor(){
	$.ajax({
			type: "GET",
			url: baseuri + "/api/" + "detailsensorreadings",
			dataType: "json",
			headers: {
				"Authorization": "Basic " + btoa(username + ":" + password)
			},
			success: function (data){
				$("#response").prepend(JSON.stringify(data) + '</br>');
				toastr.success("Left: " + data.detailsensorreadings[0] + " cms,"
					+ "Left1: " + data.detailsensorreadings[1] + " cms,"
					+ "Straight: " + data.detailsensorreadings[2] + " cms,"
					+ "Right1: " + data.detailsensorreadings[2] + " cms,"
					+ "Right: " + data.detailsensorreadings[3] + " cms"
				, 'IOT Robot Sensor');
			},
			error: function(xhr, status, error) {
				toastr.error("Status: " + status + " Error: " + error, "Oops!")
			}
	});
}


function CallControlApi(control){
	$.ajax({
		type: "GET",
		url: baseuri + "/api/" + control,
		dataType: "json",
		headers: {
			"Authorization": "Basic " + btoa(username + ":" + password)
		},
		success: function (data){
			$("#response").prepend(JSON.stringify(data) + '</br>');
			var msg = '';
			msg =  control + "Done";
			
			toastr.success(msg, 'IOT Robot');
	    },
		error: function(xhr, status, error) {
			toastr.error('Error in calling: ' + control + " Status: " + status + " Error: " + error, "Oops!")
		}
	});

	
}

function CallMovementApi(control){
	$.ajax({
		type: "GET",
		url: baseuri + "/api/move/"+ control,
		dataType: "json",
		data : {
			"value": control
		},
		headers: {
			"Authorization": "Basic " + btoa(username + ":" + password)
		},
		success: function (data){
			$("#response").prepend(JSON.stringify(data) + '</br>');
			var msg = '';
			msg = 'Camera moving ' + control + ' degree';
			
			toastr.success(msg, 'IOT Robot');
	    },
		error: function(xhr, status, error) {
			toastr.error('Error in calling: ' + control + " Status: " + status + " Error: " + error, "Oops!")
		}
	});

	
}
