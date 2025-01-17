import yaml
import os

from mcstasscript.data.data import McStasData
from mcstasscript.helper.managed_mcrun import ManagedMcrun


def name_search(name, data_list):
    """"
    name_search returns McStasData instance with specific name if it is
    in the given data_list. If no match is found, a search for the data
    filename is performed. If several matches are found, a list of
    McStasData objects are returned.

    The index of certain datasets in the data_list can change if
    additional monitors are added so it is more convinient to access
    the data files using their names.

    Parameters
    ----------
    name : string
        Name of the dataset to be retrived (component_name)

    data_list : List of McStasData instances
        List of datasets to search
    """
    if type(data_list) is not list:
        raise InputError(
            "name_search function needs list of McStasData as input")

    if not type(data_list[0]) == McStasData:
        raise InputError(
            "name_search function needs objects of type McStasData as input.")

    # Search by component name
    list_result = []
    for check in data_list:
        if check.name == name:
            list_result.append(check)

    if len(list_result) == 0:
        # Search by filename
        for check in data_list:
            if check.metadata.filename == name:
                list_result.append(check)
    
    if len(list_result) == 0:
        raise NameError("No dataset with name: \""
                        + name
                        + "\" found.")

    if len(list_result) == 1:
        return list_result[0]
    else:
        return list_result


def name_plot_options(name, data_list, **kwargs):
    """"
    name_plot_options passes keyword arguments to dataset with certain
    name in given data list

    Function for quickly setting plotting options on a certain dataset
    n a larger list of datasets

    Parameters
    ----------
    name : string
        Name of the dataset to be modified (component_name)

    data_list : List of McStasData instances
        List of datasets to search

    kwargs : keyword arguments
        Keyword arguments passed to set_plot_options in
        McStasPlotOptions
    """
    object_to_modify = name_search(name, data_list)
    if type(object_to_modify) is not list:                     
        object_to_modify.set_plot_options(**kwargs)
    else:
        for data_object in object_to_modify:
            data_object.set_plot_options(**kwargs)


def load_data(foldername):
    """
    Loads data from a McStas data folder including mccode.sim

    Parameters
    ----------
        foldername : string
            Name of the folder from which to load data
    """
    managed_mcrun = ManagedMcrun("dummy", foldername=foldername)
    return managed_mcrun.load_results()


class Configurator:
    """
    Class for setting the configuration file for McStasScript.
    
    Attributes
    ----------
    configuration_file_name : str
        absolute path of configuration file
        
    Methods
    -------
    set_mcstas_path(string)
        sets mcstas path
        
    set_mcrun_path(string)
        sets mcrun path
        
    set_line_length(int)
        sets maximum line length to given int
    
    _write_yaml(dict)
        internal method, writes a configuration yaml file with dict content
        
    _read_yaml()
        internal method, reads a configuration yaml file and returns a dict
    
    _create_new_config_file()
        internal method, creates default configuration file

    """

    def __init__(self, *args):
        """
        Initialization of configurator, checks that the configuration file
        actually exists, and if it does not, creates a default configuration
        file.
        
        Parameters
        ----------
        (optional) custom name : str
            Custom name for configuration file for testing purposes
        """

        if len(args) == 1:
            name = args[0]
        else:
            name = "configuration"

        # check configuration file exists
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        self.configuration_file_name = THIS_DIR + "/../" + name + ".yaml"
        if not os.path.isfile(self.configuration_file_name):
            # no config file found, write default config file
            self._create_new_config_file()

    def _write_yaml(self, dictionary):
        """
        Writes a dictionary as the new configuration file
        """
        with open(self.configuration_file_name, 'w') as yaml_file:
            yaml.dump(dictionary, yaml_file, default_flow_style=False)   

    def _read_yaml(self):
        """
        Reads yaml configuration file
        """
        with open(self.configuration_file_name, 'r') as ymlfile:
            return yaml.safe_load(ymlfile)

    def _create_new_config_file(self):
        """
        Writes a default configuration file to the package root directory
        """

        run = "/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/bin/"
        mcstas = "/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/"

        default_paths = {"mcrun_path" : run,
                         "mcstas_path" : mcstas}
        default_other = {"characters_per_line" : 93}

        default_config = {"paths" : default_paths,
                          "other" : default_other}

        self._write_yaml(default_config)

    def set_mcstas_path(self, path):
        """
        Sets the path to McStas

        Parameters
        ----------
        path : str
            Path to the mcstas directory containing "sources", "optics", ...
        """

        # read entire configuration file 
        config = self._read_yaml()

        # update mcstas_path
        config["paths"]["mcstas_path"] = path

        # write new configuration file
        self._write_yaml(config)

    def set_mcrun_path(self, path):
        """
        Sets the path to mcrun

        Parameters
        ----------
        path : str
            Path to the mcrun executable
        """

        # read entire configuration file 
        config = self._read_yaml()

        # update mcstas_path
        config["paths"]["mcrun_path"] = path

        # write new configuration file
        self._write_yaml(config)

    def set_line_length(self, line_length):
        """
        Sets maximum line length for output

        Parameters
        ----------
        line_length : int
            maximum line length for output
        """

        # read entire configuration file 
        config = self._read_yaml()

        # update mcstas_path
        config["other"]["characters_per_line"] = int(line_length)

        # write new configuration file
        self._write_yaml(config)


