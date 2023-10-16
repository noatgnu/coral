import logging

import click

from coral.data import Coral
from coral.utility import detect_delimiter_from_extension
import pandas as pd


@click.command(name="analyze")
@click.option("--unprocessed", "-u", type=click.Path(exists=True), help="Unprocessed file with sample intensity columns as well with index columns")
@click.option("--annotation", "-a", type=click.Path(exists=True), help="Annotation file with two columns one with sample column names the other is the condition or group that the samples should be assigned to.")
@click.option("--comparison", "-c", type=click.Path(exists=True), help="Comparison file with three columns the first two with the condition or group names in pair for comparison A-B and the last with the comparison label.")
@click.option("--output", "-o", type=click.Path(exists=False), help="Output file name", default="output.txt")
@click.option("--col-filter", "-f", type=float, help="Filter unprocessed data columns with missing values more than threshold", default=0.7)
@click.option("--row-filter", "-r", type=float, help="Filter unprocessed data rows with missing values more than threshold", default=0.7)
@click.option("--impute", "-i", type=str, help="Impute missing values with method", default="knn")
@click.option("--normalize", "-n", type=str, help="Normalize data with method", default="quantiles.robust")
@click.option("--aggregate-method", "-g", type=str, help="Aggregate data with method", default="MsCoreUtils::robustSummary")
@click.option("--aggregate-column", "-t", type=str, help="Column for aggregation", default="")
@click.option("--index-columns", "-x", type=str, help="Index columns delimited by comma", default="")
def main(unprocessed: str, annotation: str, comparison: str, output: str, col_filter: float, row_filter: float, impute: str, normalize: str, aggregate_method: str, aggregate_column: str, index_columns: str):
    coral = Coral()
    coral.load_unproccessed_file(unprocessed, sep=detect_delimiter_from_extension(unprocessed))
    annotation_df = pd.read_csv(annotation, sep=detect_delimiter_from_extension(annotation))
    comparison_df = pd.read_csv(comparison, sep=detect_delimiter_from_extension(comparison))
    index = index_columns.split(",")
    for i, r in annotation_df.iterrows():
        coral.add_sample(r["sample"])
        if r["condition"] not in coral.conditions:
            coral.add_condition(r["condition"])
        coral.add_condition_map(r["condition"], [r["sample"]])
    for i, r in comparison_df.iterrows():
        coral.add_comparison(r["condition_A"], r["condition_B"], r["comparison_label"])
    coral.index_columns = index
    coral.filter_missing_columns(col_filter)
    coral.prepare()
    coral.filter_missing_rows(row_filter)
    coral.impute(impute)
    coral.log_transform()
    if aggregate_column:
        coral.aggregate_features(aggregate_column, aggregate_method)
    coral.normalize(normalize)
    coral.prepare_for_limma()
    result = []
    for d in coral.run_limma():
        result.append(d)
    if len(result) > 1:
        result = pd.concat(result)
    else:
        result = result[0]
    result.to_csv(output, sep="\t", index=False)

if __name__ == "__main__":
    main()