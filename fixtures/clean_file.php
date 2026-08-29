<?php

declare(strict_types=1);

namespace Acme\SafePlugin;

final class HealthCheck {
    public function status(): string {
        return 'ok';
    }
}

function acme_health_check(): string {
  return (new HealthCheck())->status();
}
