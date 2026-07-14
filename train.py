import torch
import torch.nn as nn
import torch.optim as optim

def train_epoch(model, loader, optimizer, loss_fn, device):
    """One training epoch — returns (avg_loss, accuracy)."""
    model.train()
    total_loss, correct = 0, 0
    for texts, labels in loader:
        texts, labels = texts.to(device), labels.to(device)
        optimizer.zero_grad()
        out  = model(texts)
        loss = loss_fn(out, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n

def evaluate(model, loader, loss_fn, device):
    """Evaluate model — returns (avg_loss, accuracy)."""
    model.eval()
    total_loss, correct = 0, 0
    with torch.no_grad():
        for texts, labels in loader:
            texts, labels = texts.to(device), labels.to(device)
            out  = model(texts)
            loss = loss_fn(out, labels)
            total_loss += loss.item() * len(labels)
            correct    += (out.argmax(1) == labels).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n

def run_training(model, train_loader, test_loader, epochs=10, lr=5.0):
    """Full training run with scheduler."""
    device    = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model     = model.to(device)
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
    loss_fn   = nn.CrossEntropyLoss()

    print(f"Training on {device} for {epochs} epochs...")
    print(f"{'Epoch':<8} {'Train Acc':<12} {'Test Acc'}")
    print("─" * 32)

    for epoch in range(1, epochs + 1):
        _, tr_acc = train_epoch(model, train_loader, optimizer, loss_fn, device)
        _, te_acc = evaluate(model,   test_loader,  loss_fn,   device)
        scheduler.step()
        print(f"  [{epoch:02d}/{epochs}]   {tr_acc*100:.1f}%        {te_acc*100:.1f}%")

    torch.save(model.state_dict(), "rnn_model.pth")
    print("\n✓ Model saved: rnn_model.pth")
    return model
