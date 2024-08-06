<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="user.TestDAO" %>
<%@ page import="user.TestDTO" %>
<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.Arrays" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width" , initial-scale="1">
<link rel="stylesheet" href="css/bootstrap.css">
<meta http-equiv="Refresh" content="5">
<title>집중도 분석 AI</title>
 <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script>
</head>
<body>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
    integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
    crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
    integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
    crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
    integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
    crossorigin="anonymous"></script>
	<%
	ArrayList<TestDTO> list = new ArrayList<>();
		String[] array = new String[0];
		float[] array2 = new float[0];
		float[] array3 = new float[0];
		float[] array4 = new float[0];
		float[] array5 = new float[0];
		int[] array6 = new int[0];
		int[] array7 = new int[0];
		
		TestDAO testDAO = new TestDAO();
		list = testDAO.getAllTestData();
		
		array = new String[list.size()];
		array2 = new float[list.size()];
		array3 = new float[list.size()];
		array4 = new float[list.size()];
		array5 = new float[list.size()];
		array6 = new int[list.size()];
		array7 = new int[list.size()];
		
		for (int i = 0; i < list.size(); i++) {
			array[i] = list.get(i).getDatetime();
			array2[i] = list.get(i).getRight_x_movemont();
			array3[i] = list.get(i).getRight_y_movemont();
			array4[i] = list.get(i).getLeft_x_movemont();
			array5[i] = list.get(i).getLeft_y_movemont();
			array6[i] = list.get(i).getPercent();
			array7[i] = list.get(i).getTarget();
			
			
		}
		int lastValueOfArray6 = array6[array6.length - 1];
		
		int maxIndex = 0; // 최고점의 인덱스
	    int maxValue = Integer.MIN_VALUE; // 최고점의 값

	    for (int i = 0; i < list.size(); i++) {
	        array6[i] = list.get(i).getPercent();

	        // 최고점 갱신
	        if (array6[i] > maxValue) {
	            maxValue = array6[i];
	            maxIndex = i;
	        }
	    }
	%>

	
	<nav class="navbar navbar-default navbar-inverse">
		<div class="navbar-header navbar-inverse">
			<button type="button" class="navbar-toggle collapsed"
			data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"
			aria-expended="false">
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</button>
			<a class="navbar-brand " href="main3.jsp">집중도 분석 보기</a>
			<a class="navbar-brand " href="main2.jsp">눈동자 움직임 보기</a>
			</div>
       <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1"
       				aria-expanded="false">
		</div>
	</nav>
	<div class="col-lg-4 container">
        <div class="jumbotron">
        <canvas id="myChart5" width="400" height="400"></canvas>
		<script>
	        var ctx5 = document.getElementById('myChart5').getContext('2d');
	        var data5 = [];
	        var labels5 = [];
	        
	        <%for ( int s=0 ; s<list.size(); s++ ){%>
	        data5.push('<%=array6[s]%>')
	        labels5.push('<%=array[s]%>')
	        <%}%>
	       
	        
	        var chart = new Chart(ctx5, {
	            type: 'line',
	            data: {
	                labels: labels5,
	                datasets: [{
	                    label: '집중도 퍼센트',
	                    backgroundColor: 'transparent',
	                    borderColor: 'red',
	                    data: data5
	                }]
	            },
	            options: {}
	        });
   
	    </script>
        </div>
        </div> 
        

      <div class="col-lg-4 container">
        <div class="jumbotron">
        <canvas id="myChart" width="400" height="400"></canvas>
		<script>
			var ctx = document.getElementById('myChart').getContext('2d');
			var data = [0, 0]; // 초기값으로 0으로 설정
			var labels = ['집중X', '집중O'];
	
			<% for (int s = 0; s < list.size(); s++) { %>
			  var targetValue = <%= array7[s] %>;
			  data[targetValue]++; // 타겟 데이터가 1이면 1 증가, 0이면 0 증가
			<% } %>
	
			var chart = new Chart(ctx, {
			  type: 'bar',
			  data: {
			    labels: labels,
			    datasets: [{
			      label: '집중 판별',
			      backgroundColor: 'rgba(75, 192, 192, 0.2)', // 막대의 색상
			      borderColor: 'rgba(75, 192, 192, 1)', // 막대의 테두리 색상
			      borderWidth: 1, // 테두리 두께
			      data: data
			    }]
			  },
			  options: {
			        scales: {
			          yAxes: [{
			            ticks: {
			              beginAtZero: true
			            }
			          }]
			        }
			      }
			    });
        
	    </script>
        </div>
        </div>
	<div class="col-lg-4 container">
        <div class="jumbotron">
            <h2 class="text-center">집중도 상태</h2>
            <p><br>
            <p class="text-center">현재 집중도: <%=lastValueOfArray6%>%</p>
            <p class="text-center">최고점: <%= maxValue %> (시간: <%= array[maxIndex] %>)</p>

            <div id="concentrationStatus" class="text-center" style="margin-top: 20px;"></div>

            <script>
                var concentrationStatus = document.getElementById('concentrationStatus');

                // 최초 집중도 상태 표시
                updateConcentrationStatus(<%= array6[array6.length - 1] %>);

                function updateConcentrationStatus(concentration) {
                    concentrationStatus.innerHTML = '집중도 상태: ';

                    if (concentration <= 30) {
                    	concentrationStatus.style.color = 'red';
                        concentrationStatus.style.backgroundColor = 'pink';
                        concentrationStatus.innerHTML += ' 매우 나쁨';
                    } else if (concentration <= 70) {
                    	concentrationStatus.style.color = 'purple';
                        concentrationStatus.style.backgroundColor = 'lavender';
                        concentrationStatus.innerHTML += ' 나쁨';
                    } else if (concentration <= 90) {
                        concentrationStatus.style.color = 'black';
                        concentrationStatus.style.backgroundColor = 'white';
                        concentrationStatus.innerHTML += ' 평범';
                    } else {
                        concentrationStatus.style.color = 'green';
                        concentrationStatus.style.backgroundColor = 'lightgreen';
                        concentrationStatus.innerHTML += ' 좋음';
                    }
                }

                // 집중도 업데이트 시 호출
                function updateConcentration(newConcentration) {
                    updateConcentrationStatus(newConcentration);
                }
            </script>
            <p><br><br><br>
        </div>
    </div>     
        

	<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
	<script src="js/bootstrap.js"></script>
	
	<%@ include file="footer.jsp"%>	
</body>
</html>