def resolve_labels(assembly):
    labels = {}
    resolved = []

    # First pass: find label address
    addr = 0
    for line in assembly:
        if ":" in line:
            label = line.replace(":", "")
            labels[label] = addr
        else:
            addr += 1

    # Second pass: replace labels
    for line in assembly:
        if ":" in line:
            continue

        for label in labels:
            if label in line:
                line = line.replace(label, str(labels[label]))

        resolved.append(line)

    return resolved