#!/usr/bin/env python3
"""Generate IPC test files with per-batch custom_metadata.

Requires PyArrow >= 11.0.0:
    uv venv && uv pip install pyarrow && uv run python generate_custom_metadata.py
"""

import pyarrow as pa

schema = pa.schema([
    pa.field("id", pa.int32()),
    pa.field("name", pa.utf8()),
])

batch0 = pa.record_batch(
    [pa.array([1, 2, 3]), pa.array(["a", "b", "c"])],
    schema=schema,
)
batch1 = pa.record_batch(
    [pa.array([4, 5]), pa.array(["d", "e"])],
    schema=schema,
)

metadata0 = {b"batch_index": b"0", b"source": b"test"}
metadata1 = {b"batch_index": b"1", b"source": b"test"}

# --- IPC File format ---
with pa.OSFile("custom_metadata.arrow_file", "wb") as sink:
    writer = pa.ipc.new_file(sink, schema)
    writer.write_batch(batch0, custom_metadata=metadata0)
    writer.write_batch(batch1, custom_metadata=metadata1)
    writer.close()

# --- IPC Stream format ---
with pa.OSFile("custom_metadata.arrow_stream", "wb") as sink:
    writer = pa.ipc.new_stream(sink, schema)
    writer.write_batch(batch0, custom_metadata=metadata0)
    writer.write_batch(batch1, custom_metadata=metadata1)
    writer.close()

print("Generated custom_metadata.arrow_file and custom_metadata.arrow_stream")
