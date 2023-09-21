# questions DB constants
FIELD_NAME = 'field_name'
QID = "qid"
GPT_QUESTION = "gpt_question"
EXAMPLE_ANSWER = "example_answer"
PROTOCOL_QUESTION = "protocol_question"
TOKENS_PER_ANSWER = 'tokens_per_answer'
TOKENS_PER_QUESTIONS = 'tokens_per_questions'
#
best_5p_fields = ['Add_lay_back', 'Add_lay_front',
                  'Backcontact_deposition_procedure',
                  'Backcontact_stack_sequence', 'Cell_architecture',
                  'Cell_area_measured', 'Cell_flexible',
                  'Cell_number_of_cells_per_substrate', 'Cell_semitransparent',
                  'Cell_semitransparent_wavelength_range',
                  'Cell_stack_sequence', 'EQE_measured',
                  'ETL_deposition_procedure', 'ETL_stack_sequence',
                  'Encapsulation', 'HTL_stack_sequence',
                  'JV_average_over_n_number_of_cells', 'JV_certified_values',
                  'JV_default_Jsc', 'JV_default_Jsc_scan_direction',
                  'JV_default_PCE', 'JV_default_PCE_scan_direction',
                  'JV_light_intensity', 'JV_light_masked_cell',
                  'JV_light_wavelength_range', 'JV_measured',
                  'JV_reverse_scan_PCE', 'Module',
                  'Module_JV_data_recalculated_per_cell',
                  'Module_number_of_cells_in_module',
                  'Outdoor_PCE_burn_in_observed',
                  'Outdoor_average_over_n_number_of_cells',
                  'Outdoor_detaild_weather_data_available',
                  'Outdoor_installation_number_of_solar_tracking_axis',
                  'Outdoor_irradiance_measured',
                  'Outdoor_location_coordinates',
                  'Outdoor_periodic_JV_measurements',
                  'Outdoor_potential_bias_range',
                  'Outdoor_spectral_data_available',
                  'Outdoor_temperature_range', 'Outdoor_tested',
                  'Outdoor_time_end', 'Outdoor_time_start',
                  'Perovskite_band_gap_graded',
                  'Perovskite_composition_a_ions',
                  'Perovskite_composition_a_ions_coefficients',
                  'Perovskite_composition_b_ions',
                  'Perovskite_composition_b_ions_coefficients',
                  'Perovskite_composition_c_ions',
                  'Perovskite_composition_c_ions_coefficients',
                  'Perovskite_composition_inorganic',
                  'Perovskite_composition_leadfree',
                  'Perovskite_composition_long_form',
                  'Perovskite_composition_perovskite_ABC3_structure',
                  'Perovskite_composition_perovskite_inspired_structure',
                  'Perovskite_composition_short_form',
                  'Perovskite_deposition_aggregation_state_of_reactants',
                  'Perovskite_deposition_number_of_deposition_steps',
                  'Perovskite_deposition_procedure',
                  'Perovskite_deposition_quenching_induced_crystallisation',
                  'Perovskite_deposition_solvent_annealing',
                  'Perovskite_deposition_solvents', 'Perovskite_dimension_0D',
                  'Perovskite_dimension_2D',
                  'Perovskite_dimension_2D3D_mixture',
                  'Perovskite_dimension_3D',
                  'Perovskite_dimension_3D_with_2D_capping_layer',
                  'Perovskite_dimension_list_of_layers',
                  'Perovskite_single_crystal', 'Ref_DOI_number', 'Ref_ID',
                  'Ref_ID_temp', 'Ref_data_entered_by_author', 'Ref_journal',
                  'Ref_lead_author', 'Ref_name_of_person_entering_the_data',
                  'Ref_original_filename_data_upload',
                  'Ref_part_of_initial_dataset', 'Ref_publication_date',
                  'Stabilised_performance_measured',
                  'Stability_PCE_burn_in_observed',
                  'Stability_average_over_n_number_of_cells',
                  'Stability_flexible_cell_number_of_bending_cycles',
                  'Stability_light_UV_filter',
                  'Stability_light_wavelength_range', 'Stability_measured',
                  'Stability_periodic_JV_measurements',
                  'Stability_potential_bias_range',
                  'Stability_relative_humidity_range',
                  'Stability_temperature_range', 'Substrate_stack_sequence']

"""
This is the list of fields in the DB with their corresponding question in the 
form
"""
best_5p_fields_to_questions = {
    'Substrate_stack_sequence': 'Substrate. Stack sequence [Mat.1; Mat.2; '
                                '... | Mat.3; ... | Mat.4 | ...]',
    'Stability_temperature_range': 'Stability. Temperature. Range [T.min; '
                                   'T.max] or [T.constant] [deg. C]',
    'Stability_relative_humidity_range': 'Stability. Relative humidity. '
                                         'Range [RH.min; RH.max] [%]',
    'Stability_potential_bias_range': 'Stability. Potential bias. Range [U.min; U.max] or [U.constant] [V]',
    'Stability_periodic_JV_measurements': 'Stability. Periodic JV '
                                          'measurements [TRUE/FALSE]',
    'Stability_measured': 'Stability. Measured [TRUE/FALSE]',
    'Stability_light_wavelength_range': 'Stability. Light. Wavelength range '
                                        '[lambda min; lambda max] or [lambda '
                                        'constant] [nm]',
    'Stability_light_UV_filter': 'Stability. Light. UV filter [TRUE/FALSE]',
    'Stability_flexible_cell_number_of_bending_cycles': 'Stability. Flexible '
                                                        'cell. Number of '
                                                        'bending cycles',
    'Stability_average_over_n_number_of_cells': 'Stability. Average over N '
                                                'number of cells',
    'Stability_PCE_burn_in_observed': 'Stability. PCE. Burn in observed ['
                                      'TRUE/FALSE]',
    'Stabilised_performance_measured': 'Stabilised performance. Measured ['
                                       'TRUE/FALSE]',
    'Ref_publication_date': 'Ref. Publication date [year:mm:dd]',
    'Ref_part_of_initial_dataset': None,
    'Ref_original_filename_data_upload': None,
    'Ref_name_of_person_entering_the_data': 'Ref. Name of person entering '
                                            'the data',
    'Ref_lead_author': 'Ref. Lead author',
    'Ref_journal': None,
    'Ref_data_entered_by_author': 'Ref. Data entered by author [TRUE/FALSE]',
    'Ref_ID_temp': 'Ref. ID temp (Integer starting from 1 and counting upwards)',
    'Ref_ID': None,
    'Ref_DOI_number': 'Ref. DOI number',
    'Perovskite_single_crystal': 'Perovskite. Single crystal [TRUE/FALSE]',
    'Perovskite_dimension_list_of_layers': 'Perovskite. Dimension. List of '
                                           'layers [Dim.1 | Dim.2 | …]',
    'Perovskite_dimension_3D_with_2D_capping_layer': 'Perovskite. Dimension. '
                                                     '3D'
                                                     'with 2D capping layer '
                                                     '[TRUE/FALSE]',
    'Perovskite_dimension_3D': 'Perovskite. Dimension. 3D [TRUE/FALSE]',
    'Perovskite_dimension_2D3D_mixture': 'Perovskite. Dimension. 2D/3D '
                                         'mixture [TRUE/FALSE]',
    'Perovskite_dimension_2D': 'Perovskite. Dimension. 2D [TRUE/FALSE]',
    'Perovskite_dimension_0D': 'Perovskite. Dimension. 0D (Quantum dot) ['
                               'TRUE/FALSE]',
    'Perovskite_deposition_solvents': 'Perovskite. Deposition. Solvents ['
                                      'Sol.1; Sol.2 >> Sol.3; ... >> ... | '
                                      'Sol.4 >> … | Sol.5 | ... ]',
    'Perovskite_deposition_solvent_annealing': 'Perovskite. Deposition. '
                                               'Solvent annealing [TRUE/FALSE]',
    'Perovskite_deposition_quenching_induced_crystallisation':
        'Perovskite. Deposition. Quenching induced crystallisation [TRUE/FALSE]',
    'Add_lay_back': 'Add. Lay. Back [TRUE/FALSE]',
    'Add_lay_front': 'Add. Lay. Front [TRUE/FALSE]',
    'Backcontact_deposition_procedure': 'Backcontact. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]',
    'Backcontact_stack_sequence': 'Backcontact. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]',
    'Cell_architecture': 'Cell. Architecture [nip/pin/ …]',
    'Cell_area_measured': 'Cell. Area. Measured [cm^2]',
    'Cell_flexible': 'Cell. Flexible [TRUE/FALSE]',
    'Cell_number_of_cells_per_substrate': 'Cell. Number of cells per substrate',
    'Cell_semitransparent': 'Cell. Semitransparent [TRUE/FALSE]',
    'Cell_semitransparent_wavelength_range': 'Cell. Semitransparent. Average visible transmittance. Wavelength range [lambda_min; lambda_max]',
    'Cell_stack_sequence': 'Cell. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]',
    'EQE_measured': 'EQE. Measured [TRUE/FALSE]',
    'ETL_deposition_procedure': 'ETL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]',
    'ETL_stack_sequence': 'ETL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]',
    'Encapsulation': 'Encapsulation [TRUE/FALSE]',
    'HTL_stack_sequence': 'HTL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]',
    'JV_average_over_n_number_of_cells': 'JV. Average over N number of cells',
    'JV_certified_values': 'JV. Certified values [TRUE/FALSE]',
    'JV_default_Jsc': None,
    'JV_default_Jsc_scan_direction': None,
    'JV_default_PCE': None,
    'JV_default_PCE_scan_direction': None,
    'JV_light_intensity': 'JV. Light. Intensity [mW/cm^2]',
    'JV_light_masked_cell': 'JV. Light. Masked cell [TRUE/FALSE]',
    'JV_light_wavelength_range': 'JV. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm]',
    'JV_measured': 'JV. Measured [TRUE/FALSE]',
    'JV_reverse_scan_PCE': 'JV. Reverse scan. PCE [%]',
    'Module': 'Module [TRUE/FALSE]',
    'Module_JV_data_recalculated_per_cell': 'Module. JV data recalculated per cell [TRUE/FALSE]',
    'Module_number_of_cells_in_module': 'Module. Number of cells in module',
    'Outdoor_PCE_burn_in_observed': 'Outdoor. PCE. Burn in observed [TRUE/FALSE]',
    'Outdoor_average_over_n_number_of_cells': 'Outdoor. Average over N number of cells',
    'Outdoor_detaild_weather_data_available': 'Outdoor. Detaild weather data available [TRUE/FALSE]',
    'Outdoor_installation_number_of_solar_tracking_axis': 'Outdoor. Installation. Number of solar tracking axis [0/1/2]',
    'Outdoor_irradiance_measured': 'Outdoor. Irradiance measured [TRUE/FALSE]',
    'Outdoor_location_coordinates': 'Outdoor. Location. Coordinates [Latitude; Longitude] [decimal degrees]',
    'Outdoor_periodic_JV_measurements': 'Outdoor. Periodic JV measurements [TRUE/FALSE]',
    'Outdoor_potential_bias_range': 'Outdoor. Potential bias. Range [U.min; U.max] or [U.constant] [V]',
    'Outdoor_spectral_data_available': 'Outdoor. Spectral data available [TRUE/FALSE]',
    'Outdoor_temperature_range': 'Outdoor. Temperature. Range [T.min; T.max] or [T.constant] [deg. C]',
    'Outdoor_tested': 'Outdoor. Tested [TRUE/FALSE]',
    'Outdoor_time_end': 'Outdoor. Time. End [year:mm:dd:hh:mm]',
    'Outdoor_time_start': 'Outdoor. Time. Start [year:mm:dd:hh:mm]',
    'Perovskite_band_gap_graded': 'Perovskite. Band gap. Graded [TRUE/FALSE | TRUE/FALSE | ...]',
    'Perovskite_composition_a_ions': 'Perovskite. Composition. A-ions [Ion.1; Ion.2; … | Ion.3; … | ...]',
    'Perovskite_composition_a_ions_coefficients': 'Perovskite. Composition. A-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]',
    'Perovskite_composition_b_ions': 'Perovskite. Composition. B-ions [Ion.1; Ion.2; … | Ion.3; … | ...]',
    'Perovskite_composition_b_ions_coefficients': 'Perovskite. Composition. B-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]',
    'Perovskite_composition_c_ions': 'Perovskite. Composition. C-ions [Ion.1; Ion.2; … | Ion.3; … | ...]',
    'Perovskite_composition_c_ions_coefficients': 'Perovskite. Composition. C-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]',
    'Perovskite_composition_inorganic': 'Perovskite. Composition. Inorganic perovskite [TRUE/FALSE]',
    'Perovskite_composition_leadfree': 'Perovskite. Composition. Lead free [TRUE/FALSE]',
    'Perovskite_composition_long_form': None,
    'Perovskite_composition_perovskite_ABC3_structure': 'Perovskite. Composition. Perovskite ABC3 structure [TRUE/FALSE]',
    'Perovskite_composition_perovskite_inspired_structure': 'Perovskite. Composition. Perovskite inspired structure [TRUE/FALSE]',
    'Perovskite_composition_short_form': None,
    'Perovskite_deposition_aggregation_state_of_reactants': 'Perovskite. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]',
    'Perovskite_deposition_number_of_deposition_steps': 'Perovskite. Deposition. Number of deposition steps',
    'Perovskite_deposition_procedure': 'Perovskite. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]',
}

best_5p_question_to_field= {'Substrate. Stack sequence [Mat.1; Mat.2; ... | '
                            'Mat.3; ... | Mat.4 | ...]':
                                'Substrate_stack_sequence', 'Stability. '
                                                            'Temperature. '
                                                            'Range [T.min; '
                                                            'T.max] or ['
                                                            'T.constant] ['
                                                            'deg. C]':
    'Stability_temperature_range', 'Stability. Relative humidity. Range ['
                                   'RH.min; RH.max] [%]':
    'Stability_relative_humidity_range', 'Stability. Potential bias. Range ['
                                         'U.min; U.max] or [U.constant] ['
                                         'V]':
    'Stability_potential_bias_range', 'Stability. Periodic JV measurements ['
                                      'TRUE/FALSE]':
    'Stability_periodic_JV_measurements', 'Stability. Measured ['
                                          'TRUE/FALSE]':
    'Stability_measured', 'Stability. Light. Wavelength range [lambda min; '
                          'lambda max] or [lambda constant] [nm]':
    'Stability_light_wavelength_range', 'Stability. Light. UV filter ['
                                        'TRUE/FALSE]':
    'Stability_light_UV_filter', 'Stability. Flexible cell. Number of '
                                 'bending cycles':
    'Stability_flexible_cell_number_of_bending_cycles', 'Stability. Average '
                                                        'over N number of '
                                                        'cells':
    'Stability_average_over_n_number_of_cells', 'Stability. PCE. Burn in '
                                                'observed [TRUE/FALSE]':
    'Stability_PCE_burn_in_observed', 'Stabilised performance. Measured ['
                                      'TRUE/FALSE]':
    'Stabilised_performance_measured', 'Ref. Publication date [year:mm:dd]':
    'Ref_publication_date', None: 'Perovskite_composition_short_form',
                            'Ref. Name of person entering the data':
                                'Ref_name_of_person_entering_the_data',
                            'Ref. Lead author': 'Ref_lead_author',
                            'Ref. Data entered by author [TRUE/FALSE]':
                                'Ref_data_entered_by_author', 'Ref. ID temp '
                                                              '(Integer '
                                                              'starting from '
                                                              '1 and '
                                                              'counting '
                                                              'upwards)':
                                'Ref_ID_temp', 'Ref. DOI number':
                                'Ref_DOI_number', 'Perovskite. Single '
                                                  'crystal [TRUE/FALSE]':
                                'Perovskite_single_crystal', 'Perovskite. '
                                                             'Dimension. '
                                                             'List of layers '
                                                             '[Dim.1 | Dim.2 '
                                                             '| …]':
                                'Perovskite_dimension_list_of_layers',
                            'Perovskite. Dimension. 3Dwith 2D capping layer '
                            '[TRUE/FALSE]':
                                'Perovskite_dimension_3D_with_2D_capping_layer',
                            'Perovskite. Dimension. 3D [TRUE/FALSE]': 'Perovskite_dimension_3D',
                            'Perovskite. Dimension. 2D/3D mixture [TRUE/FALSE]': 'Perovskite_dimension_2D3D_mixture', 'Perovskite. Dimension. 2D [TRUE/FALSE]': 'Perovskite_dimension_2D', 'Perovskite. Dimension. 0D (Quantum dot) [TRUE/FALSE]': 'Perovskite_dimension_0D', 'Perovskite. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]': 'Perovskite_deposition_solvents', 'Perovskite. Deposition. Solvent annealing [TRUE/FALSE]': 'Perovskite_deposition_solvent_annealing', 'Perovskite. Deposition. Quenching induced crystallisation [TRUE/FALSE]': 'Perovskite_deposition_quenching_induced_crystallisation', 'Add. Lay. Back [TRUE/FALSE]': 'Add_lay_back', 'Add. Lay. Front [TRUE/FALSE]': 'Add_lay_front', 'Backcontact. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]': 'Backcontact_deposition_procedure', 'Backcontact. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]': 'Backcontact_stack_sequence', 'Cell. Architecture [nip/pin/ …]': 'Cell_architecture', 'Cell. Area. Measured [cm^2]': 'Cell_area_measured', 'Cell. Flexible [TRUE/FALSE]': 'Cell_flexible', 'Cell. Number of cells per substrate': 'Cell_number_of_cells_per_substrate', 'Cell. Semitransparent [TRUE/FALSE]': 'Cell_semitransparent', 'Cell. Semitransparent. Average visible transmittance. Wavelength range [lambda_min; lambda_max]': 'Cell_semitransparent_wavelength_range', 'Cell. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]': 'Cell_stack_sequence', 'EQE. Measured [TRUE/FALSE]': 'EQE_measured', 'ETL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]': 'ETL_deposition_procedure', 'ETL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]': 'ETL_stack_sequence', 'Encapsulation [TRUE/FALSE]': 'Encapsulation', 'HTL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]': 'HTL_stack_sequence', 'JV. Average over N number of cells': 'JV_average_over_n_number_of_cells', 'JV. Certified values [TRUE/FALSE]': 'JV_certified_values', 'JV. Light. Intensity [mW/cm^2]': 'JV_light_intensity', 'JV. Light. Masked cell [TRUE/FALSE]': 'JV_light_masked_cell', 'JV. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm]': 'JV_light_wavelength_range', 'JV. Measured [TRUE/FALSE]': 'JV_measured', 'JV. Reverse scan. PCE [%]': 'JV_reverse_scan_PCE', 'Module [TRUE/FALSE]': 'Module', 'Module. JV data recalculated per cell [TRUE/FALSE]': 'Module_JV_data_recalculated_per_cell', 'Module. Number of cells in module': 'Module_number_of_cells_in_module', 'Outdoor. PCE. Burn in observed [TRUE/FALSE]': 'Outdoor_PCE_burn_in_observed', 'Outdoor. Average over N number of cells': 'Outdoor_average_over_n_number_of_cells', 'Outdoor. Detaild weather data available [TRUE/FALSE]': 'Outdoor_detaild_weather_data_available', 'Outdoor. Installation. Number of solar tracking axis [0/1/2]': 'Outdoor_installation_number_of_solar_tracking_axis', 'Outdoor. Irradiance measured [TRUE/FALSE]': 'Outdoor_irradiance_measured', 'Outdoor. Location. Coordinates [Latitude; Longitude] [decimal degrees]': 'Outdoor_location_coordinates', 'Outdoor. Periodic JV measurements [TRUE/FALSE]': 'Outdoor_periodic_JV_measurements', 'Outdoor. Potential bias. Range [U.min; U.max] or [U.constant] [V]': 'Outdoor_potential_bias_range', 'Outdoor. Spectral data available [TRUE/FALSE]': 'Outdoor_spectral_data_available', 'Outdoor. Temperature. Range [T.min; T.max] or [T.constant] [deg. C]': 'Outdoor_temperature_range', 'Outdoor. Tested [TRUE/FALSE]': 'Outdoor_tested', 'Outdoor. Time. End [year:mm:dd:hh:mm]': 'Outdoor_time_end', 'Outdoor. Time. Start [year:mm:dd:hh:mm]': 'Outdoor_time_start', 'Perovskite. Band gap. Graded [TRUE/FALSE | TRUE/FALSE | ...]': 'Perovskite_band_gap_graded', 'Perovskite. Composition. A-ions [Ion.1; Ion.2; … | Ion.3; … | ...]': 'Perovskite_composition_a_ions', 'Perovskite. Composition. A-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]': 'Perovskite_composition_a_ions_coefficients', 'Perovskite. Composition. B-ions [Ion.1; Ion.2; … | Ion.3; … | ...]': 'Perovskite_composition_b_ions', 'Perovskite. Composition. B-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]': 'Perovskite_composition_b_ions_coefficients', 'Perovskite. Composition. C-ions [Ion.1; Ion.2; … | Ion.3; … | ...]': 'Perovskite_composition_c_ions', 'Perovskite. Composition. C-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]': 'Perovskite_composition_c_ions_coefficients', 'Perovskite. Composition. Inorganic perovskite [TRUE/FALSE]': 'Perovskite_composition_inorganic', 'Perovskite. Composition. Lead free [TRUE/FALSE]': 'Perovskite_composition_leadfree', 'Perovskite. Composition. Perovskite ABC3 structure [TRUE/FALSE]': 'Perovskite_composition_perovskite_ABC3_structure', 'Perovskite. Composition. Perovskite inspired structure [TRUE/FALSE]': 'Perovskite_composition_perovskite_inspired_structure', 'Perovskite. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]': 'Perovskite_deposition_aggregation_state_of_reactants', 'Perovskite. Deposition. Number of deposition steps': 'Perovskite_deposition_number_of_deposition_steps', 'Perovskite. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]': 'Perovskite_deposition_procedure'}