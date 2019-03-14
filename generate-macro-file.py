from macroload import load
import click

@click.command()
@click.option('--visits',type=click.Path(exists=True),required=True, help="Name of visits file in CSV format (fields arranged as Participant ID,Screening Number,Visit number,Visit date)")
@click.option('--tests',type=click.Path(exists=True),required=True,help="Name of test set file in CSV format (fields most contain test_code,var_code)")
@click.option('--data',type=click.Path(exists=True),required=True,help="Name of input data file in CSV format (fields can be configured by changing the `config.py` file)")
@click.option('--output',type=click.STRING,required=True,help="Output file for MACRO data")
def execute(visits,tests,data,output):
    """
    This is a simple script which uses pseudonymised ILAB test data to generate an output file which can be loaded into Infermed MACRO. To do this it uses three CSV-based input files.

    :param visits:
    :param tests:
    :param data:
    :param output:
    :return:
    """
    output_file = load.OutputFile(output)
    load.process_files(visits,tests,data,output_file)

if __name__ == '__main__':
    execute()
