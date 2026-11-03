# ============================================================
# Module 4: Shelf Condition Analysis
# ============================================================
# Uses simple threshold-based logic to classify each product's
# stock level as Available, Low Stock, or Out of Stock.
#
# Thresholds are defined at the top of this file and can be
# changed easily without touching any other code.
# ============================================================

from dataclasses import dataclass
from typing import Optional, List, Dict

# ─── Configurable Thresholds ─────────────────────────────────
# Adjust these values to change the stock status boundaries.
AVAILABLE_MIN_COUNT  = 5   # count >= 5  → Available
LOW_STOCK_MIN_COUNT  = 1   # count 1–4  → Low Stock (count == 0 → Out of Stock)


# ─── Data Classes ────────────────────────────────────────────

@dataclass
class StockStatus:
    AVAILABLE     = "Available"
    LOW_STOCK     = "Low Stock"
    OUT_OF_STOCK  = "Out of Stock"


@dataclass
class ProductAnalysis:
    product_name    : str
    count           : int
    avg_confidence  : Optional[float]   # None when count == 0
    status          : str               # StockStatus constant
    availability_pct: float             # 0-100 relative to AVAILABLE_MIN_COUNT


# ─── Core Analysis Logic ─────────────────────────────────────

def classify_stock(count: int, available_min: int = AVAILABLE_MIN_COUNT, low_stock_min: int = LOW_STOCK_MIN_COUNT) -> str:
    """
    Return a stock status string based on the detected product count.

    Business Rules:
        count >= available_min (5) → Available
        count >= low_stock_min (1) → Low Stock
        count == 0                 → Out of Stock
    """
    if count >= available_min:
        return StockStatus.AVAILABLE
    elif count >= low_stock_min:
        return StockStatus.LOW_STOCK
    else:
        return StockStatus.OUT_OF_STOCK


def compute_availability_pct(count: int, target_stock: int = AVAILABLE_MIN_COUNT) -> float:
    """
    Express the stock count as a percentage of the target fully-stocked
    threshold (AVAILABLE_MIN_COUNT), capped at 100 %.
    Safe against division by zero.
    """
    safe_target = max(target_stock, 1)
    return min(round((count / safe_target) * 100.0, 1), 100.0)


def analyse_shelf(
    aggregated_detections: Dict[str, dict],
    all_tracked_classes: Optional[List[str]] = None
) -> List[ProductAnalysis]:
    """
    Convert aggregated detection results into ProductAnalysis objects.

    Parameters
    ----------
    aggregated_detections : dict
        Output of utils.detection.aggregate_detections()
        Format: { "ClassName": { "count": int, "avg_conf": float, ... } }

    all_tracked_classes : list[str] | None
        Optional list of product class names to always include in the
        output (e.g. ['Coke', 'Pepsi', 'Sprite']). Classes that were
        NOT detected will appear with count=0 and status=Out of Stock.

    Returns
    -------
    list[ProductAnalysis]
        One entry per product class, sorted by count descending then name.
    """
    results: List[ProductAnalysis] = []

    # Build a merged class list maintaining order if provided
    all_classes: List[str] = []
    if all_tracked_classes:
        for c in all_tracked_classes:
            if c not in all_classes:
                all_classes.append(c)

    for c in aggregated_detections.keys():
        if c not in all_classes:
            all_classes.append(c)

    for class_name in all_classes:
        data = aggregated_detections.get(class_name, {})
        count = data.get("count", 0)
        avg_conf = data.get("avg_conf", None) if count > 0 else None

        results.append(ProductAnalysis(
            product_name     = class_name,
            count            = count,
            avg_confidence   = avg_conf,
            status           = classify_stock(count),
            availability_pct = compute_availability_pct(count),
        ))

    # Sort: highest count first, then alphabetical
    results.sort(key=lambda x: (-x.count, x.product_name))
    return results


# ─── Alert Messages ──────────────────────────────────────────

def generate_alerts(analyses: List[ProductAnalysis]) -> List[str]:
    """
    Generate plain-English restock alert messages for products
    that are Low Stock or Out of Stock. Returns an empty list
    when everything is fully stocked.
    """
    alerts = []
    for pa in analyses:
        if pa.status == StockStatus.LOW_STOCK:
            alerts.append(
                f"⚠️ **{pa.product_name}** stock is low "
                f"({pa.count} item{'s' if pa.count != 1 else ''} detected). "
                f"Restocking is recommended."
            )
        elif pa.status == StockStatus.OUT_OF_STOCK:
            alerts.append(
                f"🔴 **{pa.product_name}** is currently **out of stock** (0 items detected). "
                f"Immediate restocking required."
            )
    return alerts


# ─── Dashboard KPI Summary ───────────────────────────────────

def compute_kpis(analyses: List[ProductAnalysis], total_detected: Optional[int] = None) -> dict:
    """
    Compute the KPI numbers shown on the monitoring dashboard.

    Returns
    -------
    dict with keys:
        total_items       : int (sum of detected items)
        total_categories  : int (total tracked product categories)
        available_count   : int (categories that are fully stocked)
        low_stock_count   : int (categories that are low stock)
        out_of_stock_count: int (categories that are out of stock)
    """
    if total_detected is None:
        total_detected = sum(pa.count for pa in analyses)

    available    = sum(1 for pa in analyses if pa.status == StockStatus.AVAILABLE)
    low_stock    = sum(1 for pa in analyses if pa.status == StockStatus.LOW_STOCK)
    out_of_stock = sum(1 for pa in analyses if pa.status == StockStatus.OUT_OF_STOCK)

    return {
        "total_items"        : total_detected,
        "total_categories"   : len(analyses),
        "available_count"    : available,
        "low_stock_count"    : low_stock,
        "out_of_stock_count" : out_of_stock,
    }

