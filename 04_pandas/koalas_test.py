import databricks.koalas as ks


if __name__ == '__main__':
    # help(ks)
    # help(ks.read_csv)

    read_file = ks.read_csv("00_input/data.csv", sep='\t')
    print(read_file.head(10))
