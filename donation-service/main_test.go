package main

import (
	"encoding/json"
	"testing"
)

// Smoke test: garante que a serializacao de Donation funciona.
func TestDonationJSON(t *testing.T) {
	d := Donation{ID: 1, Amount: 10.5, Status: "APPROVED", DonorName: "Teste"}
	b, err := json.Marshal(d)
	if err != nil {
		t.Fatalf("falha ao serializar Donation: %v", err)
	}
	if len(b) == 0 {
		t.Fatal("json serializado vazio")
	}
}
