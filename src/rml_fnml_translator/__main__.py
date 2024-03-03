__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


import rdflib
import pandas as pd
import uuid
import sys

from .args_parser import load_config_from_command_line
from .constants import *
from .mapping.mapping_parser import retrieve_mappings
from .utils import get_fno_execution, replace_predicates_in_graph, get_references_in_template


function_dict = {
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#toUpperCase': {'alias': 'UPPER', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#toLowerCase': {'alias': 'LOWER', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#string_trim': {'alias': 'TRIM', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#reverse': {'alias': 'REVERSE', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#string_md5': {'alias': 'MD5', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#string_indexOf': {'alias': 'INTSTR', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#param_string_sub']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#string_replace': {'alias': 'REPLACE', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#value_find', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#value_replace']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#string_substring': {'alias': 'SUBSTRING', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#p_int_i_from', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#p_int_i_opt_to']},

    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_floor': {'alias': 'FLOOR', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_ceil': {'alias': 'CEIL', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_round': {'alias': 'ROUND', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_ln': {'alias': 'LN', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_log': {'alias': 'LOG', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_pow': {'alias': 'POW', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n_exp']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_abs': {'alias': 'ABS', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_acos': {'alias': 'ACOS', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_asin': {'alias': 'ASIN', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_atan': {'alias': 'ATAN', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_sin': {'alias': 'SIN', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#math_cos': {'alias': 'COS', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_dec_n']},

    'http://users.ugent.be/~bjdmeest/function/grel.ttl#output_datetime': {'alias': 'TODAY', 'params': []},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#date_diff': {'alias': 'DATE_DIFF', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_string_unit', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#param_string_timeunit']},
    'http://users.ugent.be/~bjdmeest/function/grel.ttl#date_datePart': {'alias': 'DATE_PART', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_date_d', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#param_datetime_d', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#param_datetime_d2']},

    'http://users.ugent.be/~bjdmeest/function/grel.ttl#controls_filter': {'alias': 'WHERE', 'params': ['http://users.ugent.be/~bjdmeest/function/grel.ttl#param_a', 'http://users.ugent.be/~bjdmeest/function/grel.ttl#uri_value']}
    # TODO: update controls_filter, not correct
}


def gen_random_id():
    return 'v'+str(uuid.uuid4()).replace('-', '')[:10]


def get_selection_projection_from_function(fno_df, fno_execution):
    projection = ''
    selection = ''

    execution_rule_df = get_fno_execution(fno_df, fno_execution)
    function_id = execution_rule_df.iloc[0]['function_map_value']

    if not function_id == 'http://users.ugent.be/~bjdmeest/function/grel.ttl#controls_filter':
        projection += function_dict[function_id]['alias'] + '('

    # handle composite functions
    for i, execution_rule in execution_rule_df.iterrows():
        if execution_rule['value_map_type'] == FNML_EXECUTION:
            rec_projection, rec_selection = get_selection_projection_from_function(fno_df, execution_rule['value_map_value'])
            if rec_projection:
                projection += rec_projection
            if rec_selection:
                selection = selection + rec_selection + ' AND '
    if selection.endswith(' AND '):
        selection = selection[:-5]

    parameter_to_value_value_dict = dict(zip(execution_rule_df['parameter_map_value'], execution_rule_df['value_map_value']))
    parameter_to_value_type_dict = dict(zip(execution_rule_df['parameter_map_value'], execution_rule_df['value_map_type']))

    # SELECTION
    if function_id == 'http://users.ugent.be/~bjdmeest/function/grel.ttl#controls_filter':
        for param in function_dict[function_id]['params']:
            # if param is not execution
            if not parameter_to_value_value_dict[param].startswith('http://'):
                # if constants use quotes
                if parameter_to_value_type_dict[param] == R2RML_CONSTANT and not parameter_to_value_type_dict[param].isnumeric():
                    selection += "'"

                selection += parameter_to_value_value_dict[param]
                if parameter_to_value_type_dict[param] == R2RML_CONSTANT and not parameter_to_value_type_dict[param].isnumeric():
                    selection += "'"
            selection += '='
        selection = selection[:-1]
    # PROJECTION
    else:
        for param in function_dict[function_id]['params']:
            # if param is not execution
            if not parameter_to_value_type_dict[param] == 'http://semweb.mmlab.be/ns/fnml#execution':
                # if constants use quotes
                if parameter_to_value_type_dict[param] == R2RML_CONSTANT:
                    projection += "'"

                projection += parameter_to_value_value_dict[param]
                if parameter_to_value_type_dict[param] == R2RML_CONSTANT:
                    projection += "'"
            elif selection:
                projection += selection.split('=')[0]
            projection += ', '
        if projection.endswith(', '):
            projection = projection[:-2]
        projection += ')'

    return projection, selection


if __name__ == "__main__":

    config = load_config_from_command_line()
    rml_df, fno_df = retrieve_mappings(config)

    ###
    # build RML (more general), and then translate to R2RML (more specific) if selected as output
    ###

    output_mapping_graph = rdflib.Graph()

    for i, mapping_rule in rml_df.iterrows():
        projection = []
        selection = []  # filter

        source_value = mapping_rule['logical_source_value']
        if mapping_rule['logical_source_value'].endswith('.csv') or mapping_rule['logical_source_value'].endswith('.parquet') or mapping_rule['logical_source_value'].endswith('.tsv'):
            source_value = f"'{mapping_rule['logical_source_value']}'"

        tm_id = rdflib.term.URIRef(mapping_rule['triples_map_id'])
        ls_id = rdflib.BNode()
        sm_id = rdflib.BNode()
        pom_id = rdflib.BNode()
        pm_id = rdflib.BNode()
        om_id = rdflib.BNode()



        ############################################################
        ##### SUBJECT MAP
        ############################################################
        output_mapping_graph.add((tm_id, rdflib.term.URIRef(R2RML_SUBJECT_MAP), sm_id))
        if mapping_rule['subject_map_type'] == FNML_EXECUTION:
            ref_id = gen_random_id()
            output_mapping_graph.add((sm_id, rdflib.term.URIRef(RML_REFERENCE), rdflib.term.Literal(ref_id)))
            f_projection, f_selection = get_selection_projection_from_function(fno_df, mapping_rule['subject_map_value'])
            if f_projection:
                projection.append(f'{f_projection} AS {ref_id}')
            if f_selection:
                selection.append(f_selection)
        else:
            output_mapping_graph.add((sm_id, rdflib.term.URIRef(mapping_rule['subject_map_type']), rdflib.term.Literal(mapping_rule['subject_map_value'])))
        if pd.notna(mapping_rule['subject_termtype']):
            output_mapping_graph.add((sm_id, rdflib.term.URIRef(R2RML_TERM_TYPE), rdflib.term.URIRef(mapping_rule['subject_termtype'])))



        ############################################################
        ##### PREDICATE OBJECT MAP
        ############################################################
        output_mapping_graph.add((tm_id, rdflib.term.URIRef(R2RML_PREDICATE_OBJECT_MAP), pom_id))

        ############################################################
        ##### PREDICATE MAP
        ############################################################
        if pd.notna(mapping_rule['predicate_map_value']):
            output_mapping_graph.add((pom_id, rdflib.term.URIRef(R2RML_PREDICATE_MAP), pm_id))

            if mapping_rule['predicate_map_type'] == FNML_EXECUTION:
                ref_id = gen_random_id()
                output_mapping_graph.add((pm_id, rdflib.term.URIRef(RML_REFERENCE), rdflib.term.Literal(ref_id)))
                f_projection, f_selection = get_selection_projection_from_function(fno_df, mapping_rule['predicate_map_value'])
                if f_projection:
                    projection.append(f'{f_projection} AS {ref_id}')
                if f_selection:
                    selection.append(f_selection)
            else:
                output_mapping_graph.add((pm_id, rdflib.term.URIRef(mapping_rule['predicate_map_type']), rdflib.term.URIRef(mapping_rule['predicate_map_value'])))

        ############################################################
        ##### OBJECT MAP
        ############################################################
        if pd.notna(mapping_rule['object_map_value']):
            output_mapping_graph.add((pom_id, rdflib.term.URIRef(R2RML_OBJECT_MAP), om_id))

            if mapping_rule['object_map_type'] == FNML_EXECUTION:
                ref_id = gen_random_id()
                output_mapping_graph.add((om_id, rdflib.term.URIRef(RML_REFERENCE), rdflib.term.Literal(ref_id)))
                f_projection, f_selection = get_selection_projection_from_function(fno_df, mapping_rule['object_map_value'])
                if f_projection:
                    projection.append(f'{f_projection} AS {ref_id}')
                if f_selection:
                    selection.append(f_selection)
            elif mapping_rule['object_map_type'] == R2RML_PARENT_TRIPLES_MAP:
                    output_mapping_graph.add((om_id, rdflib.term.URIRef(mapping_rule['object_map_type']), rdflib.term.URIRef(mapping_rule['object_map_value'])))
            else:
                output_mapping_graph.add((om_id, rdflib.term.URIRef(mapping_rule['object_map_type']), rdflib.term.Literal(mapping_rule['object_map_value'])))


            if pd.notna(mapping_rule['object_termtype']):
                output_mapping_graph.add((om_id, rdflib.term.URIRef(R2RML_TERM_TYPE), rdflib.term.URIRef(mapping_rule['object_termtype'])))
            if pd.notna(mapping_rule['object_language']):
                output_mapping_graph.add((om_id, rdflib.term.URIRef(R2RML_LANGUAGE), rdflib.term.URIRef(mapping_rule['object_language'])))
            if pd.notna(mapping_rule['object_datatype']):
                output_mapping_graph.add((om_id, rdflib.term.URIRef(R2RML_DATATYPE), rdflib.term.URIRef(mapping_rule['object_datatype'])))

        ############################################################
        ##### LOGICAL SOURCE
        ############################################################
        # complete projection
        for position in ['subject', 'predicate', 'object']:
            if mapping_rule[f'{position}_map_type'] == R2RML_TEMPLATE:
                projection.extend(get_references_in_template(mapping_rule[f'{position}_map_value']))
            elif mapping_rule[f'{position}_map_type'] == RML_REFERENCE:
                projection.append(mapping_rule[f'{position}_map_value'])


        output_mapping_graph.add((tm_id, rdflib.term.URIRef(RML_LOGICAL_SOURCE), ls_id))

        projection = list(set(projection))
        rml_view = "SELECT " + ', '.join(projection)
        rml_view += "\nFROM " + source_value
        if selection:
            rml_view += '\nWHERE ' + ' AND '.join(selection)

        output_mapping_graph.add((ls_id, rdflib.term.URIRef(RML_QUERY), rdflib.term.Literal(rml_view)))
        if source_value.endswith(".csv'") or source_value.endswith(".parquet'") or source_value.endswith(".tsv'"):
            output_mapping_graph.add((ls_id, rdflib.term.URIRef(RML_REFERENCE_FORMULATION), rdflib.term.Literal(QL_CSV)))
        else:
            output_mapping_graph.add((ls_id, rdflib.term.URIRef(RML_REFERENCE_FORMULATION), rdflib.term.Literal(R2RML_SQL2008)))

    if config.get('data_source', 'mapping_language') == 'RML':
        # already RML
        pass
    elif config.get('data_source', 'mapping_language') == 'R2RML':
        # translate to R2RML
        output_mapping_graph = replace_predicates_in_graph(output_mapping_graph, RML_QUERY, R2RML_SQL_QUERY)
        output_mapping_graph = replace_predicates_in_graph(output_mapping_graph, RML_LOGICAL_SOURCE, R2RML_LOGICAL_TABLE)
        output_mapping_graph = replace_predicates_in_graph(output_mapping_graph, RML_REFERENCE, R2RML_COLUMN)
        output_mapping_graph.remove((None, rdflib.term.URIRef(RML_REFERENCE_FORMULATION), None))
    else:
        print("The `mapping_language` option must be `RML` or `R2RML`.")
        sys.exit()

    output_mapping_graph.serialize(config.get('data_source', 'output'))
    print('###############################################################')
    print("######## [R2]RML-FNML mappings successfully translated ########")
    print('###############################################################')
