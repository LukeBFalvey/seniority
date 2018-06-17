#!/usr/bin/env python3
import seniority_lib
import pandas as pd
import sys


def generate_clean_titles(input_file):
    resolver = seniority_lib.SeniorityResolver()
    df = pd.read_csv(input_file)
    df = df[['position_title', 'position_level_code']]
    # df = df.sample(1000)
    df['title_lower'] = df.position_title.apply(lambda position_title: resolver.lower_job_title(position_title))
    df = df.dropna()
    df['title_abbreviation_resolved'] = df.title_lower.apply(lambda position_title: resolver.resolve_abbreviations(position_title))
    df = df.dropna()
    df['clean_title'] = df.title_abbreviation_resolved.apply(lambda position_title: resolver.correct_spelling(position_title))
    return df


if __name__ == '__main__':
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    df = generate_clean_titles(input_file)
    df.to_csv(output_file, index=False, encoding='utf-8')



