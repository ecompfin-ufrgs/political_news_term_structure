from data_collection.term_structure import load_and_process_term_structure_data
from vasicek import calculate_parameters_for_term_structure


def main():
    term_structure_df = load_and_process_term_structure_data(dataframe_name='economatica.xlsx')
    continuous_term_structure = calculate_parameters_for_term_structure(term_structure_df)
    
    
if __name__ == '__main__':
    main()
