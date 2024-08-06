package user;

import java.util.HashMap;

public class CommandHandler {
	HashMap<String,String> command = new HashMap<>();
	public CommandHandler() {
		command.put("login", "user.LoginCommand");
		command.put("join", "user.JoinCommand");
		command.put("logout", "user.LogoutCommand");
		command.put("write", "user.WriteCommand");
		command.put("view", "user.ViewCommand");
		command.put("update", "user.UpdateCommand");
		command.put("updatecheck", "user.UpdateCheckCommand");
		command.put("delete", "user.DeleteCommand");
	}
	Command getCommand(String cmd) {
		String strClass = command.get(cmd);
		Command cmdClass = null;
		try {
			cmdClass = (Command)Class.forName(strClass).getConstructor(null).newInstance(null);
		}catch (Exception e) {e.printStackTrace();}
		return cmdClass;
}
}