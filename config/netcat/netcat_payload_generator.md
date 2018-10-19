

## Create a payload file

bs      ->  Batch Size
Count   ->  Number of times to get bs chunks of data 

**1MB file**

    dd if=/dev/urandom of=payload1MB.dat bs=1M count=1

**10MB file**

    dd if=/dev/urandom of=payload10MB.dat bs=10M count=1

    dd if=/dev/urandom of=payload10MB.dat bs=1M count=10

**100MB file**

    dd if=/dev/urandom of=payload100MB.dat bs=100M count=1

    dd if=/dev/urandom of=payload100MB.dat bs=1M count=100