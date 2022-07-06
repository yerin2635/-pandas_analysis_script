import click

from pandas_main import (
    copy,
    cost_sum,
    service_sum,
    max_cost,
    all_company_cost_sum,
    all_company_service_cost_sum,
    filter_test,
    location_country_count,
    usage_amount_sum,
    choose_one_billing_account_id,
    month_statistics,
    print_company,
    print_company_groupby,
    cost_discount,
    cost_discount_test,
    time_test,
    groupby_time_test,
    generate_image,
    traffic_discount,
)


@click.group
def cli():
    pass


cli.add_command(copy)
cli.add_command(cost_sum)
cli.add_command(service_sum)
cli.add_command(max_cost)
cli.add_command(all_company_cost_sum)
cli.add_command(all_company_service_cost_sum)
cli.add_command(filter_test)
cli.add_command(location_country_count)
cli.add_command(usage_amount_sum)
cli.add_command(choose_one_billing_account_id)
cli.add_command(month_statistics)
cli.add_command(print_company)
cli.add_command(print_company_groupby)
cli.add_command(cost_discount)
cli.add_command(cost_discount_test)
cli.add_command(time_test)
cli.add_command(groupby_time_test)
cli.add_command(traffic_discount)
cli.add_command(generate_image)

if __name__ == "__main__":
    cli()
