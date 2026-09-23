class QuestionRouterService:
    """
    Detects common supply-chain question intents using fast,
    deterministic Python rules.

    Questions that do not match a predefined intent are routed to the
    generic analytics pipeline.
    """

    def detect_intent(self, question: str) -> str:
        normalized_question = (
            question.lower()
            .replace("-", " ")
            .replace("_", " ")
            .strip()
        )

        # ---------------------------------------------------------
        # Supplier delay-rate questions
        # Keep this before broader supplier-performance matching.
        # ---------------------------------------------------------

        if any(
            phrase in normalized_question
            for phrase in [
                "highest delay rate",
                "largest delay rate",
                "worst delay rate",
                "supplier delay rate",
                "most delayed supplier",
                "which supplier is delayed most",
            ]
        ):
            return "supplier_delay_rate"

        # ---------------------------------------------------------
        # Supplier lead-time questions
        # ---------------------------------------------------------

        if any(
            phrase in normalized_question
            for phrase in [
                "longest average lead time",
                "longest lead time",
                "highest lead time",
                "supplier lead time",
                "slowest supplier",
                "slowest replenishment",
                "takes the longest to deliver",
            ]
        ):
            return "supplier_lead_time"

        # ---------------------------------------------------------
        # Low-stock warehouse questions
        # ---------------------------------------------------------

        if any(
            phrase in normalized_question
            for phrase in [
                "low stock warehouse",
                "low stock warehouses",
                "highest low stock",
                "most low stock",
                "stockout warehouse",
                "highest risk warehouse",
                "warehouse risk",
                "low inventory warehouse",
                "inventory risk warehouse",
            ]
        ):
            return "low_stock_warehouses"

        # ---------------------------------------------------------
        # Broader supplier-performance questions
        # ---------------------------------------------------------

        if any(
            phrase in normalized_question
            for phrase in [
                "supplier performance",
                "supplier risk",
                "delivery risk",
                "highest delivery risk",
                "supplier delivery",
                "supplier delays",
                "compare suppliers",
                "supplier quality",
                "supplier otif",
                "supplier defect rate",
            ]
        ):
            return "supplier_performance"

        # ---------------------------------------------------------
        # Purchase-order questions
        # ---------------------------------------------------------

        if any(
            phrase in normalized_question
            for phrase in [
                "purchase order",
                "purchase orders",
                "open purchase orders",
                "pending purchase orders",
            ]
        ):
            return "open_purchase_orders"

        # ---------------------------------------------------------
        # Generic analytics path
        # ---------------------------------------------------------

        return "general"