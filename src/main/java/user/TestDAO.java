package user;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class TestDAO {
	Connection conn;
	private ResultSet rs;
	String url = "jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8";
	String dbID = "root";
	String dbPassword = "fhdlwp15";
	public TestDAO() {
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
			conn = DriverManager.getConnection(url,dbID,dbPassword);
		} catch (ClassNotFoundException | SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	public ArrayList<TestDTO> getAllTestData() {
        ArrayList<TestDTO> dataList = new ArrayList<>();

        try {
            String query = "SELECT * FROM testtable";
            PreparedStatement preparedStatement = conn.prepareStatement(query);
            rs = preparedStatement.executeQuery();

            while (rs.next()) {
                TestDTO testData = new TestDTO();
                testData.setDatetime(rs.getString("Datetime"));
                testData.setRight_x_movemont(rs.getFloat("right_eye_x_movement"));
                testData.setRight_y_movemont(rs.getFloat("right_eye_y_movement"));
                testData.setLeft_x_movemont(rs.getFloat("left_eye_x_movement"));
                testData.setLeft_y_movemont(rs.getFloat("left_eye_y_movement"));
                testData.setTarget(rs.getInt("target"));
                testData.setPercent(rs.getInt("percent"));
                
                // 필요한 만큼 계속해서 설정

                dataList.add(testData);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        
        }

        return dataList;
    }

		
}
