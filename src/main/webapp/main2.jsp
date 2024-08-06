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
		
		TestDAO testDAO = new TestDAO();
		list = testDAO.getAllTestData();
		
		array = new String[list.size()];
		array2 = new float[list.size()];
		array3 = new float[list.size()];
		array4 = new float[list.size()];
		array5 = new float[list.size()];
		array6 = new int[list.size()];
		
		for (int i = 0; i < list.size(); i++) {
			array[i] = list.get(i).getDatetime();
			array2[i] = list.get(i).getRight_x_movemont();
			array3[i] = list.get(i).getRight_y_movemont();
			array4[i] = list.get(i).getLeft_x_movemont();
			array5[i] = list.get(i).getLeft_y_movemont();
			array6[i] = list.get(i).getPercent();
			
		}
		int lastValueOfArray6 = array6[array6.length - 1];
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
			<a class="navbar-brand " href="main3.jsp">집중도 분석 보기 </a>
			<a class="navbar-brand " href="main2.jsp">눈동자 움직임 보기</a>
			</div>
       <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1"
       				aria-expanded="false">
		</div>
	</nav>
	<div class="col-lg-4 container">
        <div class="jumbotron">
        <canvas id="myChart5" width="300" height="300"></canvas>
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
        <canvas id="myChart" width="300" height="300"></canvas>
		<script>
	        var ctx = document.getElementById('myChart').getContext('2d');
	        var data = [];
	        var labels = [];
	        
	        <%for ( int s=0 ; s<list.size(); s++ ){%>
	        data.push('<%=array2[s]%>')
	        labels.push('<%=array[s]%>')
	        <%}%>
	       
	        
	        var chart = new Chart(ctx, {
	            type: 'line',
	            data: {
	                labels: labels,
	                datasets: [{
	                    label: '오른쪽 x좌표 움직임',
	                    backgroundColor: 'transparent',
	                    borderColor: 'red',
	                    data: data
	                }]
	            },
	            options: {}
	        });
			
	        
	        
	    </script>
        </div>
        </div>
     <div class="col-lg-4 container">
        <div class="jumbotron">
        <canvas id="myChart2" width="300" height="300"></canvas>
		<script>
	        var ctx2 = document.getElementById('myChart2').getContext('2d');
	        var data2 = [];
	        var labels2 = [];
	        
	        <%for ( int s=0 ; s<list.size(); s++ ){%>
	        data2.push('<%=array3[s]%>')
	        labels2.push('<%=array[s]%>')
	        <%}%>
	       
	        
	        var chart = new Chart(ctx2, {
	            type: 'line',
	            data: {
	                labels: labels2,
	                datasets: [{
	                    label: '오른쪽 y좌표 움직임',
	                    backgroundColor: 'transparent',
	                    borderColor: 'red',
	                    data: data2
	                }]
	            },
	            options: {}
	        });
   
	    </script>
        </div>
        </div>
        <div class="col-lg-4 container">
        <div class="jumbotron">
        <canvas id="myChart3" width="800" height="800"></canvas>
		<script>
	        var ctx3 = document.getElementById('myChart3').getContext('2d');
	        var data3 = [];
	        var labels3 = [];
	        
	        <%for ( int s=0 ; s<list.size(); s++ ){%>
	        data3.push('<%=array4[s]%>')
	        labels3.push('<%=array[s]%>')
	        <%}%>
	       
	        
	        var chart = new Chart(ctx3, {
	            type: 'line',
	            data: {
	                labels: labels3,
	                datasets: [{
	                    label: '왼쪽 x좌표 움직임',
	                    backgroundColor: 'transparent',
	                    borderColor: 'red',
	                    data: data3
	                }]
	            },
	            options: {}
	        });
   
	    </script>
        </div>
        </div>
        <div class="col-lg-4 container">
        <div class="jumbotron">
        <canvas id="myChart4" width="300" height="300"></canvas>
		<script>
	        var ctx4 = document.getElementById('myChart4').getContext('2d');
	        var data4 = [];
	        var labels4 = [];
	        
	        <%for ( int s=0 ; s<list.size(); s++ ){%>
	        data4.push('<%=array5[s]%>')
	        labels4.push('<%=array[s]%>')
	        <%}%>
	       
	        
	        var chart = new Chart(ctx4, {
	            type: 'line',
	            data: {
	                labels: labels4,
	                datasets: [{
	                    label: '왼쪽 y좌표 움직임',
	                    backgroundColor: 'transparent',
	                    borderColor: 'red',
	                    data: data4
	                }]
	            },
	            options: {}
	        });
   
	    </script>
        </div>
        </div>
        
 <div class="col-lg-4 container">
    <div class="jumbotron">
        <h2 class="text-center">사용자 눈동자 움직임 상태</h2>

        <%-- array2와 array3를 합친 후 최대값과 해당 시간을 찾는 코드 --%>
        <%
            float[] combinedArrayRightEye = new float[array2.length];
            for (int i = 0; i < array2.length; i++) {
                combinedArrayRightEye[i] = array2[i] + array3[i];
            }

            float maxCombinedValueRightEye = -Float.MAX_VALUE;
            int maxIndexRightEye = -1;

            for (int i = 0; i < combinedArrayRightEye.length; i++) {
                if (combinedArrayRightEye[i] > maxCombinedValueRightEye) {
                    maxCombinedValueRightEye = combinedArrayRightEye[i];
                    maxIndexRightEye = i;
                }
            }
        %>
		<p><br>
        <p class="text-center">오른쪽 눈동자 최대 움직임:<%= maxCombinedValueRightEye %></p>
        <p class="text-center">시간:<%= array[maxIndexRightEye] %></p>
 		<p><br>
        <%-- array4와 array5를 합친 후 최대값과 해당 시간을 찾는 코드 --%>
        <%
            float[] combinedArrayLeftEye = new float[array4.length];
            for (int i = 0; i < array4.length; i++) {
                combinedArrayLeftEye[i] = array4[i] + array5[i];
            }

            float maxCombinedValueLeftEye = -Float.MAX_VALUE;
            int maxIndexLeftEye = -1;

            for (int i = 0; i < combinedArrayLeftEye.length; i++) {
                if (combinedArrayLeftEye[i] > maxCombinedValueLeftEye) {
                    maxCombinedValueLeftEye = combinedArrayLeftEye[i];
                    maxIndexLeftEye = i;
                }
            }
        %>

        <p class="text-center">왼쪽 눈동자 최대 움직임:<%= maxCombinedValueLeftEye %></p>
        <p class="text-center">시간: <%=array[maxIndexLeftEye] %></p>

    </div>
</div>

	<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
	<script src="js/bootstrap.js"></script>
	
	<%@ include file="footer.jsp"%>	
</body>
</html>