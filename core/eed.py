class EEDComputor:

    @staticmethod
    def levenshtein_char(s1: str, s2: str) -> int:
        """
        Tính Levenshtein distance ở mức ký tự giữa hai chuỗi s1 và s2.
        """
        n, m = len(s1), len(s2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # xóa ký tự
                    dp[i][j - 1] + 1,      # chèn ký tự
                    dp[i - 1][j - 1] + cost  # thay thế ký tự
                )
        return dp[n][m]

    @staticmethod
    def levenshtein_word(s1: str, s2: str) -> int:
        """
        Tính Levenshtein distance ở mức từ (tách bằng whitespace) giữa hai chuỗi s1 và s2.
        """
        w1 = s1.split()
        w2 = s2.split()
        n, m = len(w1), len(w2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = 0 if w1[i - 1] == w2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # xóa 1 từ
                    dp[i][j - 1] + 1,      # chèn 1 từ
                    dp[i - 1][j - 1] + cost  # thay thế 1 từ
                )
        return dp[n][m]

    @staticmethod
    def compute_eed(reference: str, hypothesis: str) -> dict:
        """
        Tính EED (Edit distance normalized) giữa reference và hypothesis.

        Args:
            reference (str): Chuỗi gốc (ground-truth).
            hypothesis(str): Chuỗi transcription từ ASR.

        Returns:
            {
                'dist_char': int,    # Levenshtein distance (char-level)
                'eed_char' : float,  # EED normalized (char-level)
                'dist_word': int,    # Levenshtein distance (word-level)
                'eed_word' : float   # EED normalized (word-level)
            }
        """
        # 1. Levenshtein ở mức ký tự
        dist_c = EEDComputor.levenshtein_char(reference, hypothesis)
        eed_c  = dist_c / max(len(reference), 1)

        # 2. Levenshtein ở mức từ
        dist_w = EEDComputor.levenshtein_word(reference, hypothesis)
        num_words = len(reference.split())
        eed_w  = dist_w / max(num_words, 1)

        return {
            'dist_char': dist_c,
            'eed_char' : eed_c,
            'dist_word': dist_w,
            'eed_word' : eed_w
        }

    @staticmethod
    def report(reference: str, hypothesis: str, eed_word:bool=False, eed_char:bool=True):
        eed_results = EEDComputor.compute_eed(reference, hypothesis)

        print(f'hypothesis: {hypothesis}')
        print(f'reference: {reference}\n')

        if True == eed_char:
            print("--- CER (character-level) ---")
            print(f"Levenshtein distance (char-level): {eed_results['dist_char']}")
            print(f"CER_char (normalized): {eed_results['eed_char']:.4f}\n")

        if True == eed_word:
            print("--- CER (word-level) ---")
            print(f"Levenshtein distance (word-level): {eed_results['dist_word']}")
            print(f"CER_word (normalized): {eed_results['eed_word']:.4f}\n")
