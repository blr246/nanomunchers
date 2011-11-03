package hps.nanomunchers.architecture;

import java.util.List;

public class NanoMuncherIO implements INanoMuncherIO
{

	@Override
	public String serialize(List<MuncherPresenter> nanoMuncherRepresenters)
	{
		StringBuffer sb = new StringBuffer();
		sb.append(Integer.toString(nanoMuncherRepresenters.size()) + "\n");
		for(int i = 0;i<nanoMuncherRepresenters.size();++i)
		{
			sb.append(nanoMuncherRepresenters.get(i).toString() + "\n");
		}
		
		return sb.toString();
	}

	@Override
	public List<MuncherPresenter> deserialize(String input) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public List<MunchGraph> readInput(String filename) {
		// TODO Auto-generated method stub
		return null;
	}

}
